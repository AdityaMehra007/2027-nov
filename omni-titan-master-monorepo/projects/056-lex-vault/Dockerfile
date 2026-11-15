FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_056_lex_vault

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_056_lex_vault /app/omni_056_lex_vault
USER nonroot:nonroot
EXPOSE 9056
ENTRYPOINT ["/app/omni_056_lex_vault"]
