FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_011_nebula_run

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_011_nebula_run /app/omni_011_nebula_run
USER nonroot:nonroot
EXPOSE 9011
ENTRYPOINT ["/app/omni_011_nebula_run"]
