FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_108_starfabric_leo_mesh

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_108_starfabric_leo_mesh /app/omni_108_starfabric_leo_mesh
USER nonroot:nonroot
EXPOSE 9108
ENTRYPOINT ["/app/omni_108_starfabric_leo_mesh"]
