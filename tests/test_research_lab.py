import pytest
from pathlib import Path
from omniverse.modules.research_lab.synthesizer import AutonomousResearchLab, ResearchHypothesis, AcademicPaperDraft

def test_autonomous_hypothesis_generation():
    lab = AutonomousResearchLab()
    hyp = lab.formulate_hypothesis(
        domain="Spatial-Temporal Flood Prediction",
        baseline_metric="RMSE",
        proposed_mechanism="Graph Neural Differential Equations with Sentinel Telemetry"
    )
    
    assert isinstance(hyp, ResearchHypothesis)
    assert hyp.confidence_score > 75.0
    assert "ablation_experiments" in hyp.experimental_protocol

def test_automated_research_paper_generation(tmp_path):
    lab = AutonomousResearchLab(output_dir=tmp_path)
    paper = lab.compile_research_paper(
        title="Planetary Resilience Fabric: Federated Real-Time Geospatial Hazard Modeling with Sub-Second Consensus",
        authors=["Omniverse Autonomous Intelligence Group", "Aether Institute of Technology"],
        domain="AI for Planetary Systems"
    )
    
    assert isinstance(paper, AcademicPaperDraft)
    assert paper.output_file.exists()
    content = paper.output_file.read_text(encoding="utf-8")
    assert "Abstract" in content
    assert "Methodology" in content
    assert "Empirical Benchmarks" in content
