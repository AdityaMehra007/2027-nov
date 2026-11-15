FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_058_docu_cortex

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_058_docu_cortex /app/omni_058_docu_cortex
USER nonroot:nonroot
EXPOSE 9058
ENTRYPOINT ["/app/omni_058_docu_cortex"]
