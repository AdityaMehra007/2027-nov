//! Reference policy kernel for OMNIA.
//! This crate is a small pure decision component, not an OS kernel or a sandbox.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ActionClass {
    ReadOnly,
    Draft,
    ApprovalRequired,
    Restricted,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Decision {
    pub allowed: bool,
    pub requires_approval: bool,
}

pub fn evaluate(class: ActionClass, approved: bool) -> Decision {
    match class {
        ActionClass::ReadOnly | ActionClass::Draft => Decision {
            allowed: true,
            requires_approval: false,
        },
        ActionClass::ApprovalRequired => Decision {
            allowed: approved,
            requires_approval: true,
        },
        ActionClass::Restricted => Decision {
            allowed: false,
            requires_approval: true,
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn read_and_draft_are_allowed() {
        assert!(evaluate(ActionClass::ReadOnly, false).allowed);
        assert!(evaluate(ActionClass::Draft, false).allowed);
    }

    #[test]
    fn external_requires_approval() {
        assert!(!evaluate(ActionClass::ApprovalRequired, false).allowed);
        assert!(evaluate(ActionClass::ApprovalRequired, true).allowed);
    }

    #[test]
    fn restricted_never_allowed() {
        assert!(!evaluate(ActionClass::Restricted, true).allowed);
    }
}
