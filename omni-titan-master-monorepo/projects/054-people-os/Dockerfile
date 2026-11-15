FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_054_people_os

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_054_people_os /app/omni_054_people_os
USER nonroot:nonroot
EXPOSE 9054
ENTRYPOINT ["/app/omni_054_people_os"]
