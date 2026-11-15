FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_036_decepti_net

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_036_decepti_net /app/omni_036_decepti_net
USER nonroot:nonroot
EXPOSE 9036
ENTRYPOINT ["/app/omni_036_decepti_net"]
