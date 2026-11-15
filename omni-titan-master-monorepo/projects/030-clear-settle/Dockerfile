FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_030_clear_settle

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_030_clear_settle /app/omni_030_clear_settle
USER nonroot:nonroot
EXPOSE 9030
ENTRYPOINT ["/app/omni_030_clear_settle"]
