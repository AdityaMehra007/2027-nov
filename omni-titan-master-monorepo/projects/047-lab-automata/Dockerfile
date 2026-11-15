FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_047_lab_automata

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_047_lab_automata /app/omni_047_lab_automata
USER nonroot:nonroot
EXPOSE 9047
ENTRYPOINT ["/app/omni_047_lab_automata"]
