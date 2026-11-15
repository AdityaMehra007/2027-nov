FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_075_splat_verse

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_075_splat_verse /app/omni_075_splat_verse
USER nonroot:nonroot
EXPOSE 9075
ENTRYPOINT ["/app/omni_075_splat_verse"]
