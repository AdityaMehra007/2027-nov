FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_023_alpha_terminal

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_023_alpha_terminal /app/omni_023_alpha_terminal
USER nonroot:nonroot
EXPOSE 9023
ENTRYPOINT ["/app/omni_023_alpha_terminal"]
