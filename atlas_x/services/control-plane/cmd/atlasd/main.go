package main

import (
    "log/slog"
    "net/http"
    "os"
    "path/filepath"
    "time"

    "github.com/project-atlas/control-plane/internal/httpapi"
    "github.com/project-atlas/control-plane/internal/ledger"
    "github.com/project-atlas/control-plane/internal/store"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout,nil))
    token := os.Getenv("ATLAS_API_TOKEN")
    if len(token) < 16 { logger.Error("ATLAS_API_TOKEN must be set to at least 16 characters"); os.Exit(1) }
    dataDir := os.Getenv("ATLAS_DATA_DIR"); if dataDir == "" { dataDir = ".atlas-data" }
    log, err := ledger.Open(filepath.Join(dataDir,"audit.jsonl")); if err != nil { logger.Error("open audit ledger", "error",err); os.Exit(1) }
    defer log.Close()
    st, err := store.New(log); if err != nil { logger.Error("replay task store", "error",err); os.Exit(1) }
    addr := os.Getenv("ATLAS_ADDR"); if addr == "" { addr = "127.0.0.1:8080" }
    srv := &http.Server{Addr:addr, Handler:httpapi.New(st,log,token), ReadHeaderTimeout:5*time.Second, ReadTimeout:10*time.Second, WriteTimeout:15*time.Second, IdleTimeout:60*time.Second, MaxHeaderBytes:1<<20}
    logger.Info("ATLAS control plane starting", "addr",addr,"data_dir",dataDir)
    if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed { logger.Error("server failure", "error",err); os.Exit(1) }
}
