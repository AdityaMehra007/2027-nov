FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_010_persona_grid

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_010_persona_grid /app/omni_010_persona_grid
USER nonroot:nonroot
EXPOSE 9010
ENTRYPOINT ["/app/omni_010_persona_grid"]
