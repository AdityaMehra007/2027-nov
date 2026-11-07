package store

import (
    "crypto/rand"
    "encoding/hex"
    "encoding/json"
    "errors"
    "sort"
    "sync"
    "time"

    "github.com/project-atlas/control-plane/internal/domain"
    "github.com/project-atlas/control-plane/internal/ledger"
    "github.com/project-atlas/control-plane/internal/policy"
)

var (
    ErrNotFound = errors.New("task not found")
    ErrConflict = errors.New("task state conflict")
)

type Store struct { mu sync.RWMutex; log *ledger.Ledger; tasks map[string]domain.Task }

func New(log *ledger.Ledger) (*Store, error) {
    s := &Store{log: log, tasks: make(map[string]domain.Task)}
    for _, event := range log.Events() {
        if event.Type != "task.snapshot" { continue }
        var task domain.Task
        if err := json.Unmarshal(event.Data, &task); err != nil { return nil, err }
        s.tasks[task.ID] = task
    }
    return s, nil
}

func newID() (string, error) {
    var b [16]byte
    if _, err := rand.Read(b[:]); err != nil { return "", err }
    return hex.EncodeToString(b[:]), nil
}

func (s *Store) persist(task domain.Task, actor, note string) error {
    raw, err := json.Marshal(task)
    if err != nil { return err }
    _, err = s.log.Append(ledger.Event{Type:"task.snapshot", TaskID:task.ID, Actor:actor, Data:raw})
    return err
}

func (s *Store) Create(title, description string, class domain.ActionClass, actor string) (domain.Task, error) {
    s.mu.Lock(); defer s.mu.Unlock()
    status, err := policy.InitialStatus(class); if err != nil { return domain.Task{}, err }
    id, err := newID(); if err != nil { return domain.Task{}, err }
    now := time.Now().UTC()
    task := domain.Task{ID:id, Title:title, Description:description, ActionClass:class, Status:status, RequestedBy:actor, CreatedAt:now, UpdatedAt:now, Version:1}
    if err := task.Validate(); err != nil { return domain.Task{}, err }
    if err := s.persist(task, actor, ""); err != nil { return domain.Task{}, err }
    s.tasks[id] = task
    return task, nil
}

func (s *Store) Get(id string) (domain.Task, bool) { s.mu.RLock(); defer s.mu.RUnlock(); t, ok := s.tasks[id]; return t, ok }

func (s *Store) List() []domain.Task {
    s.mu.RLock(); defer s.mu.RUnlock()
    out := make([]domain.Task, 0, len(s.tasks))
    for _, t := range s.tasks { out = append(out, t) }
    sort.Slice(out, func(i,j int) bool { return out[i].CreatedAt.After(out[j].CreatedAt) })
    return out
}

func (s *Store) Approve(id, actor, decision, reason string) (domain.Task, error) {
    s.mu.Lock(); defer s.mu.Unlock()
    task, ok := s.tasks[id]; if !ok { return domain.Task{}, ErrNotFound }
    if task.ActionClass != domain.ActionExternal || task.Status != domain.StatusApprovalRequired { return domain.Task{}, ErrConflict }
    switch decision {
    case "approve": task.Status = domain.StatusApproved
    case "reject": task.Status = domain.StatusRejected
    default: return domain.Task{}, ErrConflict
    }
    task.ApprovedBy = actor
    task.DecisionNote = reason
    task.UpdatedAt = time.Now().UTC(); task.Version++
    if err := s.persist(task, actor, reason); err != nil { return domain.Task{}, err }
    s.tasks[id] = task
    return task, nil
}

func (s *Store) Complete(id, actor string) (domain.Task, error) {
    s.mu.Lock(); defer s.mu.Unlock()
    task, ok := s.tasks[id]; if !ok { return domain.Task{}, ErrNotFound }
    if err := policy.CanComplete(task); err != nil { return domain.Task{}, err }
    task.Status = domain.StatusCompleted
    task.UpdatedAt = time.Now().UTC(); task.Version++
    if err := s.persist(task, actor, ""); err != nil { return domain.Task{}, err }
    s.tasks[id] = task
    return task, nil
}
