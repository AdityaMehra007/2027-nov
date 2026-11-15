FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_043_trial_accelerate

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_043_trial_accelerate /app/omni_043_trial_accelerate
USER nonroot:nonroot
EXPOSE 9043
ENTRYPOINT ["/app/omni_043_trial_accelerate"]
