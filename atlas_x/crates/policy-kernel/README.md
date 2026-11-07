# ATLAS Policy Kernel

Pure, deterministic reference policy module in Rust. No `unsafe` code and no third-party dependencies.

Current capability: workspace boundary, scope checking, action-class decisions and explicit approval requirement.

This crate is not yet linked into the Go control-plane request path. Before integration, define one authoritative policy contract and add cross-language conformance tests to prevent policy drift.
