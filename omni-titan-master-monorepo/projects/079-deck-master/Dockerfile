FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_079_deck_master

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_079_deck_master /app/omni_079_deck_master
USER nonroot:nonroot
EXPOSE 9079
ENTRYPOINT ["/app/omni_079_deck_master"]
