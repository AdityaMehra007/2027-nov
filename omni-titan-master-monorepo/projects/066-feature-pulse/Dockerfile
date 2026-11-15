FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_066_feature_pulse

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_066_feature_pulse /app/omni_066_feature_pulse
USER nonroot:nonroot
EXPOSE 9066
ENTRYPOINT ["/app/omni_066_feature_pulse"]
