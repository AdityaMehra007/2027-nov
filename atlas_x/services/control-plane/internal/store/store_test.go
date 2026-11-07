package store

import (
    "path/filepath"
    "testing"
    "github.com/project-atlas/control-plane/internal/domain"
    "github.com/project-atlas/control-plane/internal/ledger"
    "github.com/project-atlas/control-plane/internal/policy"
)

func newTestStore(t *testing.T) (*Store,*ledger.Ledger) {
    t.Helper(); l,err := ledger.Open(filepath.Join(t.TempDir(),"audit.jsonl")); if err != nil { t.Fatal(err) }
    s,err := New(l); if err != nil { t.Fatal(err) }; return s,l
}

func TestExternalActionRequiresApproval(t *testing.T) {
    s,l := newTestStore(t); defer l.Close()
    task,err := s.Create("Send outreach","draft message",domain.ActionExternal,"tester"); if err != nil { t.Fatal(err) }
    if task.Status != domain.StatusApprovalRequired { t.Fatalf("status=%s",task.Status) }
    if _,err := s.Complete(task.ID,"tester"); err != policy.ErrApprovalRequired { t.Fatalf("expected approval requirement, got %v",err) }
    task,err = s.Approve(task.ID,"tester","approve","reviewed"); if err != nil { t.Fatal(err) }
    if task.Status != domain.StatusApproved { t.Fatalf("status=%s",task.Status) }
    task,err = s.Complete(task.ID,"tester"); if err != nil { t.Fatal(err) }
    if task.Status != domain.StatusCompleted { t.Fatalf("status=%s",task.Status) }
}

func TestRestrictedActionCannotBeCreated(t *testing.T) {
    s,l := newTestStore(t); defer l.Close()
    if _,err := s.Create("Transfer funds","",domain.ActionRestricted,"tester"); err != policy.ErrRestrictedAction { t.Fatalf("got %v",err) }
}

func TestStoreReplaysLedger(t *testing.T) {
    path := filepath.Join(t.TempDir(),"audit.jsonl")
    l,err := ledger.Open(path); if err != nil { t.Fatal(err) }
    s,err := New(l); if err != nil { t.Fatal(err) }
    task,err := s.Create("Read docs","",domain.ActionRead,"tester"); if err != nil { t.Fatal(err) }
    _ = l.Close()
    l2,err := ledger.Open(path); if err != nil { t.Fatal(err) }; defer l2.Close()
    s2,err := New(l2); if err != nil { t.Fatal(err) }
    got,ok := s2.Get(task.ID); if !ok || got.Title != task.Title { t.Fatal("task was not replayed") }
}
