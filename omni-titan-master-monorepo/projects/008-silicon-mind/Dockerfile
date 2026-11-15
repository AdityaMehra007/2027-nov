FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_008_silicon_mind

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_008_silicon_mind /app/omni_008_silicon_mind
USER nonroot:nonroot
EXPOSE 9008
ENTRYPOINT ["/app/omni_008_silicon_mind"]
