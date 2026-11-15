all: build test

build:
	cargo build --workspace

test:
	cargo test --workspace

server:
	cargo run -p omni-omega-server

audit:
	python tests/test_omni_singularity_112.py
