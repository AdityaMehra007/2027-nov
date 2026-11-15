FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_060_field_command

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_060_field_command /app/omni_060_field_command
USER nonroot:nonroot
EXPOSE 9060
ENTRYPOINT ["/app/omni_060_field_command"]
