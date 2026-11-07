package ledger

import (
    "bufio"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "errors"
    "fmt"
    "os"
    "path/filepath"
    "sync"
    "time"
)

type Event struct {
    Sequence uint64 `json:"sequence"`
    Type string `json:"type"`
    TaskID string `json:"task_id"`
    Actor string `json:"actor"`
    Timestamp time.Time `json:"timestamp"`
    Data json.RawMessage `json:"data"`
    PreviousHash string `json:"previous_hash"`
    Hash string `json:"hash"`
}

type Ledger struct {
    mu sync.Mutex
    file *os.File
    events []Event
    head string
}

var ErrCorruptLedger = errors.New("audit ledger integrity verification failed")

func Open(path string) (*Ledger, error) {
    if err := os.MkdirAll(filepath.Dir(path), 0o700); err != nil { return nil, err }
    f, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR|os.O_APPEND, 0o600)
    if err != nil { return nil, err }
    l := &Ledger{file: f}
    scanner := bufio.NewScanner(f)
    scanner.Buffer(make([]byte, 4096), 2*1024*1024)
    var previous string
    var sequence uint64
    for scanner.Scan() {
        var event Event
        if err := json.Unmarshal(scanner.Bytes(), &event); err != nil { f.Close(); return nil, fmt.Errorf("decode ledger: %w", err) }
        if event.Sequence != sequence+1 || event.PreviousHash != previous { f.Close(); return nil, ErrCorruptLedger }
        expected, err := calculateHash(event)
        if err != nil { f.Close(); return nil, err }
        if expected != event.Hash { f.Close(); return nil, ErrCorruptLedger }
        previous = event.Hash
        sequence = event.Sequence
        l.events = append(l.events, event)
    }
    if err := scanner.Err(); err != nil { f.Close(); return nil, err }
    l.head = previous
    return l, nil
}

func calculateHash(event Event) (string, error) {
    event.Hash = ""
    raw, err := json.Marshal(event)
    if err != nil { return "", err }
    sum := sha256.Sum256(raw)
    return hex.EncodeToString(sum[:]), nil
}

func (l *Ledger) Append(event Event) (Event, error) {
    l.mu.Lock()
    defer l.mu.Unlock()
    event.Sequence = uint64(len(l.events)+1)
    event.Timestamp = time.Now().UTC()
    event.PreviousHash = l.head
    hash, err := calculateHash(event)
    if err != nil { return Event{}, err }
    event.Hash = hash
    raw, err := json.Marshal(event)
    if err != nil { return Event{}, err }
    raw = append(raw, '\n')
    n, err := l.file.Write(raw)
    if err != nil { return Event{}, err }
    if n != len(raw) { return Event{}, errors.New("short write to audit ledger") }
    if err := l.file.Sync(); err != nil { return Event{}, err }
    l.events = append(l.events, event)
    l.head = event.Hash
    return event, nil
}

func (l *Ledger) Events() []Event {
    l.mu.Lock(); defer l.mu.Unlock()
    out := make([]Event, len(l.events))
    copy(out, l.events)
    return out
}

func (l *Ledger) Verify() (int, string, error) {
    l.mu.Lock(); defer l.mu.Unlock()
    var previous string
    for i, event := range l.events {
        if event.Sequence != uint64(i+1) || event.PreviousHash != previous { return len(l.events), l.head, ErrCorruptLedger }
        expected, err := calculateHash(event)
        if err != nil { return len(l.events), l.head, err }
        if expected != event.Hash { return len(l.events), l.head, ErrCorruptLedger }
        previous = event.Hash
    }
    return len(l.events), l.head, nil
}

func (l *Ledger) Close() error { return l.file.Close() }
