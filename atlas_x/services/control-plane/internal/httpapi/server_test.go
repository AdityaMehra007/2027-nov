package httpapi

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "path/filepath"
    "testing"
    "github.com/project-atlas/control-plane/internal/ledger"
    "github.com/project-atlas/control-plane/internal/store"
)

func setup(t *testing.T) http.Handler {
    t.Helper(); l,err := ledger.Open(filepath.Join(t.TempDir(),"audit.jsonl")); if err != nil { t.Fatal(err) }
    t.Cleanup(func(){ _ = l.Close() })
    s,err := store.New(l); if err != nil { t.Fatal(err) }
    return New(s,l,"a-test-token-that-is-long-enough")
}

func TestAuthAndExternalApprovalFlow(t *testing.T) {
    h := setup(t)
    unauth := httptest.NewRecorder(); h.ServeHTTP(unauth,httptest.NewRequest("GET","/v1/tasks",nil))
    if unauth.Code != 401 { t.Fatalf("unauth status %d",unauth.Code) }
    body := []byte(`{"title":"Send an email","action_class":"external"}`)
    req := httptest.NewRequest("POST","/v1/tasks",bytes.NewReader(body)); req.Header.Set("Authorization","Bearer a-test-token-that-is-long-enough"); req.Header.Set("Content-Type","application/json")
    rr := httptest.NewRecorder(); h.ServeHTTP(rr,req)
    if rr.Code != 201 { t.Fatalf("create status %d: %s",rr.Code,rr.Body.String()) }
    var task map[string]any; if err := json.Unmarshal(rr.Body.Bytes(),&task); err != nil { t.Fatal(err) }
    id := task["id"].(string)
    complete := httptest.NewRequest("POST","/v1/tasks/"+id+"/complete",nil); complete.Header.Set("Authorization","Bearer a-test-token-that-is-long-enough")
    cr := httptest.NewRecorder(); h.ServeHTTP(cr,complete); if cr.Code != 403 { t.Fatalf("complete before approval=%d",cr.Code) }
    approve := httptest.NewRequest("POST","/v1/tasks/"+id+"/approval",bytes.NewBufferString(`{"decision":"approve","reason":"reviewed"}`)); approve.Header.Set("Authorization","Bearer a-test-token-that-is-long-enough"); approve.Header.Set("Content-Type","application/json")
    ar := httptest.NewRecorder(); h.ServeHTTP(ar,approve); if ar.Code != 200 { t.Fatalf("approval=%d %s",ar.Code,ar.Body.String()) }
}
