package policy

import (
    "errors"
    "github.com/project-atlas/control-plane/internal/domain"
)

var (
    ErrRestrictedAction = errors.New("restricted action class is not executable")
    ErrApprovalRequired = errors.New("explicit approval is required")
    ErrInvalidTransition = errors.New("invalid task state transition")
)

func InitialStatus(class domain.ActionClass) (domain.TaskStatus, error) {
    switch class {
    case domain.ActionRead, domain.ActionDraft:
        return domain.StatusOpen, nil
    case domain.ActionExternal:
        return domain.StatusApprovalRequired, nil
    case domain.ActionRestricted:
        return "", ErrRestrictedAction
    default:
        return "", ErrInvalidTransition
    }
}

func CanComplete(task domain.Task) error {
    if task.Status == domain.StatusCompleted || task.Status == domain.StatusRejected {
        return ErrInvalidTransition
    }
    if task.ActionClass == domain.ActionRestricted { return ErrRestrictedAction }
    if task.ActionClass == domain.ActionExternal && task.Status != domain.StatusApproved {
        return ErrApprovalRequired
    }
    if task.Status != domain.StatusOpen && task.Status != domain.StatusApproved {
        return ErrInvalidTransition
    }
    return nil
}
