FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_035_shield_waf

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_035_shield_waf /app/omni_035_shield_waf
USER nonroot:nonroot
EXPOSE 9035
ENTRYPOINT ["/app/omni_035_shield_waf"]
