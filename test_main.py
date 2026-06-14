# test_main.py
import pytest
from unittest.mock import patch
from main import main


# ── Helper ────────────────────────────────────────────────────────────────────

def run_main_with_inputs(*inputs):
    """Simulate user inputs and return printed output."""
    with patch("builtins.input", side_effect=list(inputs)):
        with patch("builtins.print") as mock_print:
            main()
            return " ".join(str(call) for call in mock_print.call_args_list)


# ── Menu / Navigation ─────────────────────────────────────────────────────────

class TestMenu:
    def test_exit_choice(self, capsys):
        with patch("builtins.input", side_effect=["5"]):
            main()
        captured = capsys.readouterr()
        assert "exiting" in captured.out.lower()

    def test_invalid_choice(self, capsys):
        with patch("builtins.input", side_effect=["9", "5"]):
            main()
        captured = capsys.readouterr()
        assert "invalid choice" in captured.out.lower()

    def test_menu_displays_options(self, capsys):
        with patch("builtins.input", side_effect=["5"]):
            main()
        captured = capsys.readouterr()
        assert "1" in captured.out
        assert "2" in captured.out
        assert "3" in captured.out
        assert "4" in captured.out
        assert "5" in captured.out


# ── Add Task (choice 1) ───────────────────────────────────────────────────────

class TestMainAddTask:
    def test_add_valid_task(self, capsys):
        with patch("builtins.input", side_effect=["1", "Buy milk", "From the store", "2026-12-01", "2", "5"]):
            main()
        captured = capsys.readouterr()
        assert "successfully" in captured.out.lower()

    def test_add_task_invalid_title(self, capsys):
        with patch("builtins.input", side_effect=["1", "", "Desc", "2026-12-01", "2", "5"]):
            main()
        captured = capsys.readouterr()
        assert "successfully" not in captured.out.lower()

    def test_add_task_invalid_date(self, capsys):
        with patch("builtins.input", side_effect=["1", "Title", "Desc", "bad-date", "2", "5"]):
            main()
        captured = capsys.readouterr()
        assert "successfully" not in captured.out.lower()

    def test_add_task_invalid_priority(self, capsys):
        with patch("builtins.input", side_effect=["1", "Title", "Desc", "2026-12-01", "9", "5"]):
            main()
        captured = capsys.readouterr()
        assert "successfully" not in captured.out.lower()


# ── Mark Task as Complete (choice 2) ─────────────────────────────────────────

class TestMainMarkComplete:
    def test_mark_task_complete(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Task 1", "Desc", "2026-12-01", "2",  # add task
            "2", "1",                                    # mark complete
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        assert "complete" in captured.out.lower()

    def test_mark_task_invalid_index(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Task 1", "Desc", "2026-12-01", "2",  # add task
            "2", "99",                                   # bad index
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        assert "invalid" in captured.out.lower()

    def test_mark_task_non_numeric_index(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Task 1", "Desc", "2026-12-01", "2",  # add task
            "2", "abc",                                  # non-numeric
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        assert "invalid" in captured.out.lower()


# ── View Pending Tasks (choice 3) ────────────────────────────────────────────

class TestMainViewPending:
    def test_view_pending_shows_pending_tasks(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Pending Task", "Desc", "2026-12-01", "2",  # add task
            "3",                                               # view pending
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        assert "Pending Task" in captured.out

    def test_view_pending_hides_complete_tasks(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Done Task", "Desc", "2026-12-01", "2",  # add task
            "2", "1",                                       # mark complete
            "3",                                            # view pending
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        # "Done Task" should not appear in pending view
        pending_section = captured.out.split("View Pending")[-1]
        assert "Done Task" not in pending_section

    def test_view_pending_empty(self, capsys):
        with patch("builtins.input", side_effect=["3", "5"]):
            main()
        captured = capsys.readouterr()
        # should not crash and nothing printed for tasks
        assert "Task Management" in captured.out


# ── View Progress (choice 4) ──────────────────────────────────────────────────

class TestMainViewProgress:
    def test_progress_zero_when_no_tasks(self, capsys):
        with patch("builtins.input", side_effect=["4", "5"]):
            main()
        captured = capsys.readouterr()
        assert "0.00%" in captured.out

    def test_progress_100_when_all_complete(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Task 1", "Desc", "2026-12-01", "2",  # add
            "2", "1",                                    # complete
            "4",                                         # progress
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        assert "100.00%" in captured.out

    def test_progress_50_when_half_complete(self, capsys):
        with patch("builtins.input", side_effect=[
            "1", "Task 1", "Desc", "2026-12-01", "2",  # add
            "1", "Task 2", "Desc", "2026-12-01", "2",  # add
            "2", "1",                                    # complete task 1
            "4",                                         # progress
            "5"
        ]):
            main()
        captured = capsys.readouterr()
        assert "50.00%" in captured.out

    def test_progress_output_format(self, capsys):
        with patch("builtins.input", side_effect=["4", "5"]):
            main()
        captured = capsys.readouterr()
        assert "Progress:" in captured.out