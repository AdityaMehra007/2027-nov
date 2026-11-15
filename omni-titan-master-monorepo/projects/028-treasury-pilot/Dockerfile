FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_028_treasury_pilot

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_028_treasury_pilot /app/omni_028_treasury_pilot
USER nonroot:nonroot
EXPOSE 9028
ENTRYPOINT ["/app/omni_028_treasury_pilot"]
