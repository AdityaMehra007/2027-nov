FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_006_synth_forge

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_006_synth_forge /app/omni_006_synth_forge
USER nonroot:nonroot
EXPOSE 9006
ENTRYPOINT ["/app/omni_006_synth_forge"]
