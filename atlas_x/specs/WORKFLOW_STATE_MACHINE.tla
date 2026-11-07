---------------- MODULE AtlasWorkflow ----------------
EXTENDS Naturals, TLC

CONSTANTS Read, Draft, External, Restricted,
          Open, ApprovalRequired, Approved, Rejected, Completed

VARIABLES actionClass, status, approvalGranted, effectExecuted
vars == <<actionClass, status, approvalGranted, effectExecuted>>

Init ==
    /\ actionClass \in {Read, Draft, External, Restricted}
    /\ status = IF actionClass = External THEN ApprovalRequired ELSE Open
    /\ approvalGranted = FALSE
    /\ effectExecuted = FALSE

Approve ==
    /\ actionClass = External
    /\ status = ApprovalRequired
    /\ approvalGranted' = TRUE
    /\ status' = Approved
    /\ UNCHANGED <<actionClass, effectExecuted>>

Reject ==
    /\ actionClass = External
    /\ status = ApprovalRequired
    /\ status' = Rejected
    /\ approvalGranted' = FALSE
    /\ UNCHANGED <<actionClass, effectExecuted>>

Complete ==
    /\ status \in {Open, Approved}
    /\ (actionClass # External \/ approvalGranted)
    /\ actionClass # Restricted
    /\ status' = Completed
    /\ effectExecuted' = TRUE
    /\ UNCHANGED <<actionClass, approvalGranted>>

Next == Approve \/ Reject \/ Complete

SafetyNoUnapprovedExternalEffect ==
    actionClass = External /\ effectExecuted => approvalGranted

SafetyRestrictedNeverExecutes ==
    actionClass = Restricted => ~effectExecuted

Spec == Init /\ [][Next]_vars
====================================================
