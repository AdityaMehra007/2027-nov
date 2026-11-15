FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_088_agri_precision

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_088_agri_precision /app/omni_088_agri_precision
USER nonroot:nonroot
EXPOSE 9088
ENTRYPOINT ["/app/omni_088_agri_precision"]
