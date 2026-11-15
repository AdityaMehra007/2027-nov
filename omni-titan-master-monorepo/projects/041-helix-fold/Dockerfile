FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_041_helix_fold

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_041_helix_fold /app/omni_041_helix_fold
USER nonroot:nonroot
EXPOSE 9041
ENTRYPOINT ["/app/omni_041_helix_fold"]
