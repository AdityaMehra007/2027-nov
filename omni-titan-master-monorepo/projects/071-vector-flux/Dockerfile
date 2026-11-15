FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_071_vector_flux

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_071_vector_flux /app/omni_071_vector_flux
USER nonroot:nonroot
EXPOSE 9071
ENTRYPOINT ["/app/omni_071_vector_flux"]
