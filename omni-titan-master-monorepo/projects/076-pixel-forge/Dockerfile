FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_076_pixel_forge

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_076_pixel_forge /app/omni_076_pixel_forge
USER nonroot:nonroot
EXPOSE 9076
ENTRYPOINT ["/app/omni_076_pixel_forge"]
