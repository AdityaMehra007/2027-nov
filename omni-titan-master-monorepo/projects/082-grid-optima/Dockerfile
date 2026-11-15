FROM rust:1.82-bookworm AS builder
WORKDIR /workspace
COPY . .
RUN cargo build --release -p omni_082_grid_optima

FROM gcr.io/distroless/cc-debian12:nonroot
COPY --from=builder /workspace/target/release/omni_082_grid_optima /app/omni_082_grid_optima
USER nonroot:nonroot
EXPOSE 9082
ENTRYPOINT ["/app/omni_082_grid_optima"]
