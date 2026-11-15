FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_090_build_track

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_090_build_track /app/omni_090_build_track
USER nonroot:nonroot
EXPOSE 9090
ENTRYPOINT ["/app/omni_090_build_track"]
