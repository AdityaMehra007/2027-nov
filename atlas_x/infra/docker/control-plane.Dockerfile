FROM golang:1.23-alpine AS build
WORKDIR /src
COPY services/control-plane ./services/control-plane
WORKDIR /src/services/control-plane
RUN CGO_ENABLED=0 go build -trimpath -ldflags="-s -w" -o /out/atlasd ./cmd/atlasd

FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /app
COPY --from=build /out/atlasd /app/atlasd
EXPOSE 8080
ENTRYPOINT ["/app/atlasd"]
