import React, { useState } from 'react';
export const Dashboard: React.FC = () => {
  const [p, setP] = useState(16);
  const [s, setS] = useState(4);
  const [out, setOut] = useState('');
  const run = async () => {
    const r = await fetch('/api/v1/execute', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tenant_id: 'omni-sovereign', primary_input: p, secondary_input: s })
    });
    setOut(JSON.stringify(await r.json(), null, 2));
  };
  return (
    <div style={{ padding: 24 }}>
      <h2>#111 TOPOLOGICAL-QPU-CODE // 2D Surface Code Stabilizer Syndrome MWPM Decoder</h2>
      <p>Category: FRONTIER_QUANTUM | Displaces: IBM Quantum / Google Sycamore | Metric: logical_qubits_error_corrected</p>
      <input type="number" value={p} onChange={e => setP(Number(e.target.value))} />
      <input type="number" value={s} onChange={e => setS(Number(e.target.value))} />
      <button onClick={run}>Execute logical_qubits_error_corrected</button>
      <pre>{out}</pre>
    </div>
  );
};
