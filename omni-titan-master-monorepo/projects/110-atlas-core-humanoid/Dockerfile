FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_110_atlas_core_humanoid

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_110_atlas_core_humanoid /app/omni_110_atlas_core_humanoid
USER nonroot:nonroot
EXPOSE 9110
ENTRYPOINT ["/app/omni_110_atlas_core_humanoid"]
