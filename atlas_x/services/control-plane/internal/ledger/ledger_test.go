package ledger

import (
    "encoding/json"
    "os"
    "path/filepath"
    "testing"
)

func TestHashChainDetectsMutation(t *testing.T) {
    path := filepath.Join(t.TempDir(),"audit.jsonl")
    l,err := Open(path); if err != nil { t.Fatal(err) }
    data,_ := json.Marshal(map[string]string{"value":"one"})
    if _,err := l.Append(Event{Type:"test",TaskID:"x",Actor:"tester",Data:data}); err != nil { t.Fatal(err) }
    if _,_,err := l.Verify(); err != nil { t.Fatal(err) }
    if err := l.Close(); err != nil { t.Fatal(err) }
    raw,err := os.ReadFile(path); if err != nil { t.Fatal(err) }
    for i := range raw { if raw[i] == 'o' { raw[i] = 'X'; break } }
    if err := os.WriteFile(path,raw,0o600); err != nil { t.Fatal(err) }
    if _,err := Open(path); err == nil { t.Fatal("expected tamper detection") }
}
