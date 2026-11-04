from pathlib import Path

def test_prompt_no1_sync():
    path = Path("PROMPT_NO1_2027.md")
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "UNIVERSAL_MASTER_DIRECTIVE_2027.md" in content
    assert "12 Planetary Services" in content
