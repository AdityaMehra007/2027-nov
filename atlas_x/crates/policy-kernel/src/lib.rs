#![forbid(unsafe_code)]

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ActionClass { Read, Draft, External, Restricted }
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision { Allow, RequireApproval, Deny }

pub struct Subject<'a> { pub authenticated: bool, pub workspace_id: &'a str, pub scopes: &'a [&'a str] }
pub struct Request<'a> { pub workspace_id: &'a str, pub action_class: ActionClass, pub approval_granted: bool }

fn has_scope(subject: &Subject<'_>, scope: &str) -> bool {
    subject.scopes.iter().any(|candidate| *candidate == scope)
}

pub fn authorize(subject: &Subject<'_>, request: &Request<'_>) -> Decision {
    if !subject.authenticated || subject.workspace_id != request.workspace_id { return Decision::Deny; }
    match request.action_class {
        ActionClass::Read => if has_scope(subject, "atlas:read") || has_scope(subject, "atlas:write") { Decision::Allow } else { Decision::Deny },
        ActionClass::Draft => if has_scope(subject, "atlas:write") { Decision::Allow } else { Decision::Deny },
        ActionClass::External => {
            if !has_scope(subject, "atlas:external") { Decision::Deny }
            else if request.approval_granted { Decision::Allow } else { Decision::RequireApproval }
        }
        ActionClass::Restricted => Decision::Deny,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn cross_workspace_is_denied() {
        let s = Subject { authenticated:true, workspace_id:"a", scopes:&["atlas:read"] };
        let r = Request { workspace_id:"b", action_class:ActionClass::Read, approval_granted:false };
        assert_eq!(authorize(&s,&r),Decision::Deny);
    }
    #[test] fn external_requires_approval() {
        let s = Subject { authenticated:true, workspace_id:"a", scopes:&["atlas:external"] };
        let r = Request { workspace_id:"a", action_class:ActionClass::External, approval_granted:false };
        assert_eq!(authorize(&s,&r),Decision::RequireApproval);
    }
    #[test] fn restricted_is_denied() {
        let s = Subject { authenticated:true, workspace_id:"a", scopes:&["atlas:external"] };
        let r = Request { workspace_id:"a", action_class:ActionClass::Restricted, approval_granted:true };
        assert_eq!(authorize(&s,&r),Decision::Deny);
    }
}
