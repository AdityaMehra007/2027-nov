# Multi-stage production build for Omni-Titan Sovereign Monorepo
FROM rust:1.80-bullseye AS chef
RUN cargo install cargo-chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release --bin omni-omega-server --bin omni-cli

FROM gcr.io/distroless/cc-debian12 AS runtime
WORKDIR /app
COPY --from=builder /app/target/release/omni-omega-server /app/omni-omega-server
COPY --from=builder /app/target/release/omni-cli /app/omni-cli
EXPOSE 8000 9090
USER 10001:10001
ENTRYPOINT ["/app/omni-omega-server"]
