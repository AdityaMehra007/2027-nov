FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_104_hyperspanner_erasuredb

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_104_hyperspanner_erasuredb /app/omni_104_hyperspanner_erasuredb
USER nonroot:nonroot
EXPOSE 9104
ENTRYPOINT ["/app/omni_104_hyperspanner_erasuredb"]
