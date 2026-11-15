use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum RaftRole {
    Follower,
    Candidate,
    Leader,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RaftNodeState {
    pub node_id: u64,
    pub current_term: u64,
    pub role: RaftRole,
    pub voted_for: Option<u64>,
    pub commit_index: u64,
    pub last_applied: u64,
}

impl RaftNodeState {
    pub fn new(node_id: u64) -> Self {
        Self {
            node_id,
            current_term: 0,
            role: RaftRole::Follower,
            voted_for: None,
            commit_index: 0,
            last_applied: 0,
        }
    }

    pub fn start_election(&mut self) {
        self.current_term += 1;
        self.role = RaftRole::Candidate;
        self.voted_for = Some(self.node_id);
    }

    pub fn become_leader(&mut self) {
        self.role = RaftRole::Leader;
    }
}
