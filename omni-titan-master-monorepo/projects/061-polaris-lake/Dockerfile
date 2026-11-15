FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_061_polaris_lake

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_061_polaris_lake /app/omni_061_polaris_lake
USER nonroot:nonroot
EXPOSE 9061
ENTRYPOINT ["/app/omni_061_polaris_lake"]
