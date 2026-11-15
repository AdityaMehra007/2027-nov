FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_078_motion_rig

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_078_motion_rig /app/omni_078_motion_rig
USER nonroot:nonroot
EXPOSE 9078
ENTRYPOINT ["/app/omni_078_motion_rig"]
