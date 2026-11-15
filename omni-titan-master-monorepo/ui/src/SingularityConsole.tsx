import React, { useState } from 'react';

interface FrontierCard {
  id: number;
  name: string;
  era: string;
  moat: string;
}

const FRONTIER_12: FrontierCard[] = [
  { id: 101, name: 'ChronosVM-Prover', era: 'PAST -> FUTURE', moat: 'Linear-Scan SSA & Formal Bounds Prover' },
  { id: 102, name: 'Aethelgard-LiquidAGI', era: 'POST-TRANSFORMER', moat: 'Liquid Time-Constant ODE & MCTS PUCT' },
  { id: 103, name: 'QuantumVault-LWE-STARK', era: 'POST-QUANTUM', moat: 'Kyber GF(3329) NTT & zk-STARK FRI Folder' },
  { id: 104, name: 'HyperSpanner-ErasureDB', era: 'PLANETARY STORAGE', moat: 'Zero-2PC Sequencer & GF(2^8) Reed-Solomon' },
  { id: 105, name: 'CitadelOmega-MM', era: 'SOVEREIGN QUANT', moat: 'Avellaneda-Stoikov HJB Optimal Market Maker' },
  { id: 106, name: 'HeliosFusion-MPC', era: 'FUSION ENERGY', moat: 'Lawson Triple-Product & Tokamak LQR Control' },
  { id: 107, name: 'BioGenesis-RNA-CRISPR', era: 'PROGRAMMABLE BIO', moat: 'Nussinov O(N^3) RNA Folder & Codon Optimizer' },
  { id: 108, name: 'StarFabric-LEO-Mesh', era: 'ORBITAL SPACE', moat: 'J2 Nodal Precession & Optical Laser Mesh' },
  { id: 109, name: 'FabOS-Litho-EDA', era: 'SUB-NM SILICON', moat: 'Analytical HPWL Placer & High-NA EUV Litho' },
  { id: 110, name: 'AtlasCore-Humanoid', era: 'PHYSICAL AGI', moat: 'LIPM Zero-Moment Point & Capture-Point MPC' },
  { id: 111, name: 'TopologicalQPU-Code', era: 'FAULT-TOLERANT QPU', moat: '2D Surface Code Syndrome MWPM Decoder' },
  { id: 112, name: 'SovereignCashflow-Engine', era: 'MONETIZATION CORE', moat: 'Bandit Dynamic Pricer & ASC-606 ARR Engine' },
];

export const SingularityConsole: React.FC = () => {
  const [selectedProjectId, setSelectedProjectId] = useState<number>(105);
  const [primaryInput, setPrimaryInput] = useState<number>(24);
  const [secondaryInput, setSecondaryInput] = useState<number>(6);
  const [telemetryJson, setTelemetryJson] = useState<string>(
    '// OMNI-SINGULARITY v10,000.0 ONLINE. Click any Frontier Hyper-System (#101-#112) or enter any Flagship ID (#001-#112).'
  );

  const runProject = async (id: number) => {
    setSelectedProjectId(id);
    const res = await fetch(`/api/v1/projects/${id}/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tenant_id: 'omni-singularity-sovereign',
        primary_input: primaryInput,
        secondary_input: secondaryInput,
      }),
    });
    setTelemetryJson(JSON.stringify(await res.json(), null, 2));
  };

  const runAll112 = async () => {
    const res = await fetch('/api/v1/projects/execute-all-112', { method: 'POST' });
    setTelemetryJson(JSON.stringify(await res.json(), null, 2));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-mono p-6 space-y-6">
      <header className="border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <span className="text-xs font-bold text-amber-400">
            OMNI-SINGULARITY v10,000.0 // PAST-PRESENT-FUTURE HYPER-INFRASTRUCTURE
          </span>
          <h1 className="text-xl font-bold text-white mt-1">
            100 ENTERPRISE FLAGSHIPS (#001-#100) + 12 FRONTIER HYPER-SYSTEMS (#101-#112)
          </h1>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={runAll112}
            className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded"
          >
            EXECUTE ALL 112 SYSTEMS & SEAL LEDGER
          </button>
        </div>
      </header>

      <div className="grid grid-cols-12 gap-6">
        <div className="col-span-7 space-y-4">
          <div className="flex items-center space-x-3 bg-slate-900 p-3 rounded border border-slate-800 text-xs">
            <span>Direct Project ID (1..112):</span>
            <input
              type="number"
              min={1}
              max={112}
              value={selectedProjectId}
              onChange={(e) => setSelectedProjectId(Number(e.target.value))}
              className="bg-slate-950 border border-slate-700 px-2 py-1 rounded w-20"
            />
            <span>P1:</span>
            <input
              type="number"
              value={primaryInput}
              onChange={(e) => setPrimaryInput(Number(e.target.value))}
              className="bg-slate-950 border border-slate-700 px-2 py-1 rounded w-20"
            />
            <span>P2:</span>
            <input
              type="number"
              value={secondaryInput}
              onChange={(e) => setSecondaryInput(Number(e.target.value))}
              className="bg-slate-950 border border-slate-700 px-2 py-1 rounded w-20"
            />
            <button
              onClick={() => runProject(selectedProjectId)}
              className="px-3 py-1 bg-emerald-500 text-slate-950 font-bold rounded"
            >
              Run #{String(selectedProjectId).padStart(3, '0')}
            </button>
          </div>

          <div className="grid grid-cols-3 gap-3">
            {FRONTIER_12.map((f) => (
              <button
                key={f.id}
                onClick={() => runProject(f.id)}
                className="text-left p-3.5 rounded bg-slate-900/80 hover:bg-slate-800 border border-slate-800 hover:border-amber-400 transition"
              >
                <div className="flex justify-between text-[10px] font-bold text-amber-400">
                  <span>#{f.id}</span>
                  <span>{f.era}</span>
                </div>
                <div className="text-xs font-bold text-white mt-1">{f.name}</div>
                <div className="text-[10px] text-slate-400 mt-1">{f.moat}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="col-span-5 flex flex-col">
          <div className="text-xs font-bold text-emerald-400 uppercase mb-2">
            Live Kernel Output, ASC-606 ARR Monetization & BLAKE3 Seal
          </div>
          <pre className="flex-1 bg-slate-900 border border-slate-800 rounded p-4 text-xs text-emerald-300 overflow-auto max-h-[70vh]">
            {telemetryJson}
          </pre>
        </div>
      </div>
    </div>
  );
};

export default SingularityConsole;
