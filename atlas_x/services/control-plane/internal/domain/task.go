package domain

import (
    "errors"
    "strings"
    "time"
)

type ActionClass string
const (
    ActionRead ActionClass = "read"
    ActionDraft ActionClass = "draft"
    ActionExternal ActionClass = "external"
    ActionRestricted ActionClass = "restricted"
)

type TaskStatus string
const (
    StatusOpen TaskStatus = "open"
    StatusApprovalRequired TaskStatus = "approval_required"
    StatusApproved TaskStatus = "approved"
    StatusRejected TaskStatus = "rejected"
    StatusCompleted TaskStatus = "completed"
)

type Task struct {
    ID string `json:"id"`
    Title string `json:"title"`
    Description string `json:"description,omitempty"`
    ActionClass ActionClass `json:"action_class"`
    Status TaskStatus `json:"status"`
    RequestedBy string `json:"requested_by"`
    ApprovedBy string `json:"approved_by,omitempty"`
    DecisionNote string `json:"decision_note,omitempty"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
    Version uint64 `json:"version"`
}

var ErrInvalidTask = errors.New("invalid task")

func (t *Task) Validate() error {
    t.Title = strings.TrimSpace(t.Title)
    t.Description = strings.TrimSpace(t.Description)
    if t.Title == "" || len(t.Title) > 200 { return ErrInvalidTask }
    if len(t.Description) > 8000 { return ErrInvalidTask }
    switch t.ActionClass {
    case ActionRead, ActionDraft, ActionExternal, ActionRestricted:
    default:
        return ErrInvalidTask
    }
    if strings.TrimSpace(t.RequestedBy) == "" { return ErrInvalidTask }
    return nil
}
