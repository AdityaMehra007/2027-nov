---------------- MODULE OMNIA_WORKFLOW_SAFETY ----------------
EXTENDS Naturals, FiniteSets, TLC

CONSTANTS ReadOnly, Draft, ApprovalRequired, Restricted,
          Ready, PendingApproval, Approved, Running,
          Succeeded, Failed, Cancelled

VARIABLES actionClass, state, approvalGranted

vars == <<actionClass, state, approvalGranted>>

Init ==
  /\ actionClass \in {ReadOnly, Draft, ApprovalRequired, Restricted}
  /\ state \in {Ready, PendingApproval}
  /\ approvalGranted = FALSE

RequestApproval ==
  /\ actionClass = ApprovalRequired
  /\ state = PendingApproval
  /\ UNCHANGED <<actionClass, state, approvalGranted>>

Approve ==
  /\ actionClass = ApprovalRequired
  /\ state = PendingApproval
  /\ state' = Approved
  /\ approvalGranted' = TRUE
  /\ UNCHANGED actionClass

ExecuteSafe ==
  /\ actionClass \in {ReadOnly, Draft}
  /\ state = Ready
  /\ state' = Running
  /\ UNCHANGED <<actionClass, approvalGranted>>

ExecuteApproved ==
  /\ actionClass = ApprovalRequired
  /\ state = Approved
  /\ approvalGranted = TRUE
  /\ state' = Running
  /\ UNCHANGED <<actionClass, approvalGranted>>

Complete ==
  /\ state = Running
  /\ state' = Succeeded
  /\ UNCHANGED <<actionClass, approvalGranted>>

Next ==
  \/ RequestApproval
  \/ Approve
  \/ ExecuteSafe
  \/ ExecuteApproved
  \/ Complete

Spec == Init /\ [][Next]_vars

NoRestrictedExecution ==
  actionClass = Restricted => state # Running

ApprovalBeforeExternalExecution ==
  actionClass = ApprovalRequired /\ state = Running => approvalGranted = TRUE

=============================================================
