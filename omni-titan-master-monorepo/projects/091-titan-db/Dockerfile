FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_091_titan_db

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_091_titan_db /app/omni_091_titan_db
USER nonroot:nonroot
EXPOSE 9091
ENTRYPOINT ["/app/omni_091_titan_db"]
