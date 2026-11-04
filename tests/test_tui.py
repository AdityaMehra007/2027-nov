import pytest
from omniverse.ui.tui import CyberpunkTUI
from omniverse.core.database import DatabaseEngine

def test_tui_initialization():
    tui_ansi = CyberpunkTUI(use_ansi=True)
    assert tui_ansi.use_ansi is True
    assert tui_ansi.last_command_output == "SYSTEM ONLINE // AWAITING DIRECTIVES"

    tui_no_ansi = CyberpunkTUI(use_ansi=False)
    assert tui_no_ansi.use_ansi is False

def test_tui_render_panels(tmp_path):
    db_file = tmp_path / "tui_test.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)

        header = tui.render_header()
        assert "OMNIVERSE" in header
        assert "AETHER RESILIENCE FABRIC" in header

        nodes_panel = tui.render_planetary_nodes()
        assert "NODE-BLR-01" in nodes_panel
        assert "NODE-TYO-01" in nodes_panel
        assert "NODE-IAD-01" in nodes_panel

        financial_panel = tui.render_financial_ticker()
        assert "PIPELINE VALUE" in financial_panel
        assert "COLLECTED REVENUE" in financial_panel
        assert "FX LIQUIDITY HEDGE" in financial_panel

        health_panel = tui.render_system_health()
        assert "OVERALL" in health_panel
        assert "HEALTHY" in health_panel

        cmd_bar = tui.render_command_bar()
        assert "COMMANDS:" in cmd_bar
        assert "[q] Quit" in cmd_bar

        dashboard = tui.render_dashboard()
        assert len(dashboard) > 500

def test_tui_command_handling(tmp_path):
    db_file = tmp_path / "tui_test2.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)

        # Consensus Quorum command
        res_m = tui.handle_command("m")
        assert "CONSENSUS" in res_m

        # Status refresh command
        res_s = tui.handle_command("s")
        assert "DIAGNOSTICS REFRESHED" in res_s

        # Risk pulse command
        res_r = tui.handle_command("r")
        assert "AETHER HAZARD PULSE" in res_r

        # Help command
        res_h = tui.handle_command("h")
        assert "HELP:" in res_h

        # Unknown command
        res_unk = tui.handle_command("unknown_cmd")
        assert "UNKNOWN COMMAND" in res_unk

        # Quit command
        res_q = tui.handle_command("q")
        assert res_q == "QUIT"

def test_tui_run_loop_cycles(tmp_path):
    db_file = tmp_path / "tui_test3.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)
        # Should execute exactly 2 cycles and exit without blocking
        tui.run_loop(max_cycles=2)

def test_tui_run_loop_with_input_stream(tmp_path):
    db_file = tmp_path / "tui_test4.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)
        commands = iter(["m", "s", "q"])
        tui.run_loop(input_fn=commands.__next__)
        assert "DIAGNOSTICS REFRESHED" in tui.last_command_output or "SYSTEM SHUTDOWN" in tui.last_command_output

def test_tui_panel_width_consistency(tmp_path):
    db_file = tmp_path / "tui_test5.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)
        panels = [
            ("Nodes", tui.render_planetary_nodes()),
            ("Ticker", tui.render_financial_ticker()),
            ("Health", tui.render_system_health()),
            ("Command", tui.render_command_bar())
        ]
        for name, panel in panels:
            for idx, line in enumerate(panel.split("\n")):
                assert len(line) == 76, f"Panel '{name}' line {idx} length {len(line)} != 76: {line}"

def test_tui_run_loop_piped_stdin(tmp_path, monkeypatch):
    import io
    db_file = tmp_path / "tui_test6.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)
        fake_stdin = io.StringIO("m\nq\n")
        monkeypatch.setattr("sys.stdin", fake_stdin)
        tui.run_loop()
        assert "CONSENSUS" in tui.last_command_output or "SYSTEM SHUTDOWN" in tui.last_command_output

def test_tui_run_loop_eof_stdin(tmp_path, monkeypatch):
    import io
    db_file = tmp_path / "tui_test7.db"
    db = DatabaseEngine(db_url=f"sqlite:///{db_file}")
    db.init_db()

    with db.get_session() as session:
        tui = CyberpunkTUI(session=session, use_ansi=False)
        fake_stdin = io.StringIO("")  # Immediate EOF
        monkeypatch.setattr("sys.stdin", fake_stdin)
        # Should exit gracefully without infinite loop
        tui.run_loop()

