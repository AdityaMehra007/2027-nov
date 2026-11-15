import React, { useState } from 'react';
import { SingularityConsole } from './SingularityConsole';

export const OmniOmegaPortal: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'singularity' | 'flagships'>('singularity');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-mono">
      <nav className="border-b border-slate-800 bg-slate-900/50 px-6 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <span className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="font-bold text-sm tracking-wider text-amber-400">
            CASHFLOW INFINITY // OMNI-SINGULARITY v10,000.0
          </span>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveTab('singularity')}
            className={`px-3 py-1 text-xs font-bold rounded ${
              activeTab === 'singularity' ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-slate-300'
            }`}
          >
            FRONTIER 12 HYPER-SYSTEMS
          </button>
          <button
            onClick={() => setActiveTab('flagships')}
            className={`px-3 py-1 text-xs font-bold rounded ${
              activeTab === 'flagships' ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-slate-300'
            }`}
          >
            100 ENTERPRISE FLAGSHIPS
          </button>
        </div>
      </nav>

      <main>
        {activeTab === 'singularity' ? (
          <SingularityConsole />
        ) : (
          <div className="p-8 text-center text-slate-400">
            <h2 className="text-lg font-bold text-white mb-2">100 Enterprise Flagship Fleet Active</h2>
            <p className="text-xs">Port map: 9001 (AetherOS) through 9100 (OmniOS-Web). All 100 microservices dispatched via Gateway :8090.</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default OmniOmegaPortal;
