#!/usr/bin/env python3
"""Example 06: Autonomous Academic Research Paper Synthesis.

Demonstrates mathematical envelope specification, ablation experiment design,
and automated LaTeX/Markdown scientific paper drafting.
"""

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pathlib import Path
from omniverse.modules.research_lab import AutonomousResearchLab

def main():
    print("================================================================")
    print("  06. AUTONOMOUS ACADEMIC RESEARCH LAB SYNTHESIZER")
    print("================================================================")

    lab = AutonomousResearchLab(output_dir=Path("./reports/research_papers"))

    # 1. Formulate Hypothesis
    print("\n🔬 Step 1: Formulating Scientific Hypothesis...")
    hyp = lab.formulate_hypothesis(
        domain="planetary-autonomous-resilience",
        baseline_metric="Quorum-Consensus-Latency",
        proposed_mechanism="Decentralized Byzantine Edge Mesh with WGS84 Dynamic Geohashing"
    )
    print(f" • Hypothesis ID       : {hyp.hypothesis_id}")
    print(f" • Domain              : {hyp.domain}")
    print(f" • Proposed Mechanism  : {hyp.proposed_mechanism}")
    print(f" • Prior Confidence    : {hyp.confidence_score}%")
    print(f" • Ablation Protocols  : {len(hyp.experimental_protocol['ablation_experiments'])} ablation passes configured")

    # 2. Compile Publication-Grade Paper Draft
    print("\n📄 Step 2: Compiling Peer-Review Ready Paper Draft...")
    paper = lab.generate_research_paper(
        hypothesis=hyp,
        title="Decentralized Byzantine Edge Fabrics and Planetary Satellite Logistics"
    )
    print(f" • Paper Title         : {paper.title}")
    print(f" • Co-Authors          : {', '.join(paper.authors)}")
    print(f" • Generated File      : {paper.output_file}")
    print(f"\n--- ABSTRACT PREVIEW ---")
    print(paper.abstract)
    print("================================================================")

if __name__ == "__main__":
    main()
