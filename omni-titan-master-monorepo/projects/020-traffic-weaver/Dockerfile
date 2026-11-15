FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_020_traffic_weaver

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_020_traffic_weaver /app/omni_020_traffic_weaver
USER nonroot:nonroot
EXPOSE 9020
ENTRYPOINT ["/app/omni_020_traffic_weaver"]
