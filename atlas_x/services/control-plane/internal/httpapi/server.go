package httpapi

import (
    "crypto/subtle"
    "encoding/json"
    "errors"
    "io"
    "net/http"
    "strings"

    "github.com/project-atlas/control-plane/internal/domain"
    "github.com/project-atlas/control-plane/internal/ledger"
    "github.com/project-atlas/control-plane/internal/policy"
    "github.com/project-atlas/control-plane/internal/store"
)

type Server struct { store *store.Store; ledger *ledger.Ledger; token string }
type errorBody struct { Error string `json:"error"` }
type createRequest struct { Title string `json:"title"`; Description string `json:"description"`; ActionClass domain.ActionClass `json:"action_class"` }
type approvalRequest struct { Decision string `json:"decision"`; Reason string `json:"reason"` }

func New(s *store.Store, l *ledger.Ledger, token string) http.Handler {
    api := &Server{store:s, ledger:l, token:token}
    mux := http.NewServeMux()
    mux.HandleFunc("GET /healthz", api.health)
    mux.Handle("/v1/", api.auth(http.HandlerFunc(api.routeV1)))
    return securityHeaders(mux)
}

func securityHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("Cache-Control", "no-store")
        w.Header().Set("Referrer-Policy", "no-referrer")
        next.ServeHTTP(w,r)
    })
}

func (s *Server) auth(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        got := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
        if s.token == "" || len(got) != len(s.token) || subtle.ConstantTimeCompare([]byte(got), []byte(s.token)) != 1 {
            writeError(w, http.StatusUnauthorized, "unauthorized")
            return
        }
        next.ServeHTTP(w,r)
    })
}

func actor(r *http.Request) string {
    a := strings.TrimSpace(r.Header.Get("X-Atlas-Actor"))
    if a == "" { return "local-api-operator" }
    if len(a) > 100 { return "local-api-operator" }
    return a
}

func (s *Server) health(w http.ResponseWriter, r *http.Request) { writeJSON(w,200,map[string]string{"status":"ok"}) }

func (s *Server) routeV1(w http.ResponseWriter, r *http.Request) {
    path := strings.Trim(strings.TrimPrefix(r.URL.Path,"/v1/"),"/")
    if path == "tasks" {
        if r.Method == http.MethodGet { writeJSON(w,200,map[string]any{"tasks":s.store.List()}); return }
        if r.Method == http.MethodPost { s.createTask(w,r); return }
        writeError(w,405,"method not allowed"); return
    }
    if path == "audit/verify" && r.Method == http.MethodGet {
        count, head, err := s.ledger.Verify()
        if err != nil { writeError(w,500,"audit verification failed"); return }
        writeJSON(w,200,map[string]any{"valid":true,"events":count,"head_hash":head}); return
    }
    parts := strings.Split(path,"/")
    if len(parts) == 2 && parts[0] == "tasks" && r.Method == http.MethodGet {
        task, ok := s.store.Get(parts[1]); if !ok { writeError(w,404,"task not found"); return }; writeJSON(w,200,task); return
    }
    if len(parts) == 3 && parts[0] == "tasks" && parts[2] == "approval" && r.Method == http.MethodPost { s.approve(w,r,parts[1]); return }
    if len(parts) == 3 && parts[0] == "tasks" && parts[2] == "complete" && r.Method == http.MethodPost { s.complete(w,r,parts[1]); return }
    writeError(w,404,"route not found")
}

func decode(w http.ResponseWriter, r *http.Request, dst any) error {
    r.Body = http.MaxBytesReader(w,r.Body,1<<20)
    dec := json.NewDecoder(r.Body); dec.DisallowUnknownFields()
    if err := dec.Decode(dst); err != nil { return err }
    if err := dec.Decode(&struct{}{}); err != io.EOF { return errors.New("request must contain one JSON object") }
    return nil
}

func (s *Server) createTask(w http.ResponseWriter,r *http.Request) {
    var req createRequest
    if err := decode(w,r,&req); err != nil { writeError(w,400,"invalid JSON request"); return }
    class := req.ActionClass; if class == "" { class = domain.ActionDraft }
    task, err := s.store.Create(req.Title,req.Description,class,actor(r))
    if err != nil {
        if errors.Is(err,policy.ErrRestrictedAction) { writeError(w,403,"restricted action class is prohibited"); return }
        writeError(w,400,"task validation failed"); return
    }
    writeJSON(w,201,task)
}

func (s *Server) approve(w http.ResponseWriter,r *http.Request,id string) {
    var req approvalRequest
    if err := decode(w,r,&req); err != nil { writeError(w,400,"invalid JSON request"); return }
    if len(req.Reason) > 1000 { writeError(w,400,"reason too long"); return }
    task, err := s.store.Approve(id,actor(r),req.Decision,req.Reason)
    if err != nil { writeError(w,409,err.Error()); return }
    writeJSON(w,200,task)
}

func (s *Server) complete(w http.ResponseWriter,r *http.Request,id string) {
    task, err := s.store.Complete(id,actor(r))
    if err != nil {
        status := 409
        if errors.Is(err,store.ErrNotFound) { status = 404 }
        if errors.Is(err,policy.ErrApprovalRequired) { status = 403 }
        if errors.Is(err,policy.ErrRestrictedAction) { status = 403 }
        writeError(w,status,err.Error()); return
    }
    writeJSON(w,200,task)
}

func writeJSON(w http.ResponseWriter,status int,v any) { w.Header().Set("Content-Type","application/json; charset=utf-8"); w.WriteHeader(status); _ = json.NewEncoder(w).Encode(v) }
func writeError(w http.ResponseWriter,status int,msg string) { writeJSON(w,status,errorBody{Error:msg}) }
