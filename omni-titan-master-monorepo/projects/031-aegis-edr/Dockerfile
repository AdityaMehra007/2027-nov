FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_031_aegis_edr

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_031_aegis_edr /app/omni_031_aegis_edr
USER nonroot:nonroot
EXPOSE 9031
ENTRYPOINT ["/app/omni_031_aegis_edr"]
