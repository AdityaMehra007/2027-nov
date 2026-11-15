FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_040_geo_vanguard

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_040_geo_vanguard /app/omni_040_geo_vanguard
USER nonroot:nonroot
EXPOSE 9040
ENTRYPOINT ["/app/omni_040_geo_vanguard"]
