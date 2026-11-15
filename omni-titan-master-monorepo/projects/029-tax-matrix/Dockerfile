FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_029_tax_matrix

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_029_tax_matrix /app/omni_029_tax_matrix
USER nonroot:nonroot
EXPOSE 9029
ENTRYPOINT ["/app/omni_029_tax_matrix"]
