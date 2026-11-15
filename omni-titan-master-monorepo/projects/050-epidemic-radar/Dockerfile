FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_050_epidemic_radar

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_050_epidemic_radar /app/omni_050_epidemic_radar
USER nonroot:nonroot
EXPOSE 9050
ENTRYPOINT ["/app/omni_050_epidemic_radar"]
