FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_085_factory_twin

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_085_factory_twin /app/omni_085_factory_twin
USER nonroot:nonroot
EXPOSE 9085
ENTRYPOINT ["/app/omni_085_factory_twin"]
