FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_052_rev_engine

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_052_rev_engine /app/omni_052_rev_engine
USER nonroot:nonroot
EXPOSE 9052
ENTRYPOINT ["/app/omni_052_rev_engine"]
