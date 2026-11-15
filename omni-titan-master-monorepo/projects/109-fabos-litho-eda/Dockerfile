FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_109_fabos_litho_eda

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_109_fabos_litho_eda /app/omni_109_fabos_litho_eda
USER nonroot:nonroot
EXPOSE 9109
ENTRYPOINT ["/app/omni_109_fabos_litho_eda"]
