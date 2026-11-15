FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_072_cine_cloud

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_072_cine_cloud /app/omni_072_cine_cloud
USER nonroot:nonroot
EXPOSE 9072
ENTRYPOINT ["/app/omni_072_cine_cloud"]
