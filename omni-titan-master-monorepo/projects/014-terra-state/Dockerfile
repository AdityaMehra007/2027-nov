FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_014_terra_state

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_014_terra_state /app/omni_014_terra_state
USER nonroot:nonroot
EXPOSE 9014
ENTRYPOINT ["/app/omni_014_terra_state"]
