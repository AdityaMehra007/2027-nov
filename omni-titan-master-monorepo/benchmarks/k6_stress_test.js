import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 100,
  duration: '30s',
};

export default function () {
  const projectId = Math.floor(Math.random() * 112) + 1;
  const payload = JSON.stringify({
    tenant_id: 'stress-test-bot',
    primary_input: 16,
    secondary_input: 4,
  });

  const res = http.post(`http://localhost:8090/api/v1/projects/${projectId}/execute`, payload, {
    headers: { 'Content-Type': 'application/json' },
  });

  check(res, {
    'status is 200': (r) => r.status === 200,
  });

  sleep(0.01);
}
