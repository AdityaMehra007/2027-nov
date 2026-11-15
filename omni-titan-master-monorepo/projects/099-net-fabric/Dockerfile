FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_099_net_fabric

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_099_net_fabric /app/omni_099_net_fabric
USER nonroot:nonroot
EXPOSE 9099
ENTRYPOINT ["/app/omni_099_net_fabric"]
