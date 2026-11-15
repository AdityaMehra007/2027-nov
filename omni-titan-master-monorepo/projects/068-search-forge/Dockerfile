FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_068_search_forge

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_068_search_forge /app/omni_068_search_forge
USER nonroot:nonroot
EXPOSE 9068
ENTRYPOINT ["/app/omni_068_search_forge"]
