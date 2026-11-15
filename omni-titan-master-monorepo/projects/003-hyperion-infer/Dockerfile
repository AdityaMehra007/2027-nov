FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_003_hyperion_infer

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_003_hyperion_infer /app/omni_003_hyperion_infer
USER nonroot:nonroot
EXPOSE 9003
ENTRYPOINT ["/app/omni_003_hyperion_infer"]
