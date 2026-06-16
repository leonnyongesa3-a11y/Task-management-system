# test_task_utils.py
import pytest
from task_manager.task_utils import add_task, mark_task_as_complete, view_pending_tasks, calculate_progress


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def empty_tasks():
    return []

@pytest.fixture
def sample_tasks():
    return [
        {"title": "Task 1", "description": "Desc 1", "due_date": "2026-12-01", "priority": "high", "status": "pending"},
        {"title": "Task 2", "description": "Desc 2", "due_date": "2026-12-02", "priority": "low",  "status": "complete"},
        {"title": "Task 3", "description": "Desc 3", "due_date": "2026-12-03", "priority": "medium", "status": "pending"},
    ]


# ── add_task ──────────────────────────────────────────────────────────────────

class TestAddTask:
    def test_add_task_successfully(self, empty_tasks):
        result = add_task(empty_tasks, "Buy groceries", "Milk and eggs", "2026-12-01", "high")
        assert len(result) == 1
        assert result[0]["title"] == "Buy groceries"
        assert result[0]["status"] == "pending"

    def test_add_task_returns_tasks_list(self, empty_tasks):
        result = add_task(empty_tasks, "Buy groceries", "Milk and eggs", "2026-12-01", "high")
        assert isinstance(result, list)

    def test_add_multiple_tasks(self, empty_tasks):
        add_task(empty_tasks, "Task 1", "Desc 1", "2026-12-01", "high")
        add_task(empty_tasks, "Task 2", "Desc 2", "2026-12-02", "low")
        assert len(empty_tasks) == 2

    def test_add_task_sets_pending_status(self, empty_tasks):
        result = add_task(empty_tasks, "Task", "Desc", "2026-12-01", "high")
        assert result[0]["status"] == "pending"

    def test_add_task_invalid_title(self, empty_tasks, capsys):
        result = add_task(empty_tasks, "", "Desc", "2026-12-01", "high")
        assert len(result) == 0
        captured = capsys.readouterr()
        assert captured.out != ""  # error message was printed

    def test_add_task_invalid_description(self, empty_tasks):
        result = add_task(empty_tasks, "Title", "", "2026-12-01", "high")
        assert len(result) == 0

    def test_add_task_invalid_due_date(self, empty_tasks):
        result = add_task(empty_tasks, "Title", "Desc", "not-a-date", "high")
        assert len(result) == 0

    def test_add_task_invalid_priority(self, empty_tasks):
        result = add_task(empty_tasks, "Title", "Desc", "2026-12-01", "urgent")
        assert len(result) == 0

    def test_add_task_prints_success(self, empty_tasks, capsys):
        add_task(empty_tasks, "Title", "Desc", "2026-12-01", "high")
        captured = capsys.readouterr()
        assert "successfully" in captured.out.lower()


# ── mark_task_as_complete ─────────────────────────────────────────────────────

class TestMarkTaskAsComplete:
    def test_mark_valid_task_complete(self, sample_tasks):
        result = mark_task_as_complete(sample_tasks, 1)
        assert result[0]["status"] == "complete"

    def test_mark_task_prints_success(self, sample_tasks, capsys):
        mark_task_as_complete(sample_tasks, 1)
        captured = capsys.readouterr()
        assert "complete" in captured.out.lower()

    def test_mark_task_invalid_index_too_high(self, sample_tasks, capsys):
        mark_task_as_complete(sample_tasks, 99)
        captured = capsys.readouterr()
        assert "invalid" in captured.out.lower()

    def test_mark_task_invalid_index_zero(self, sample_tasks, capsys):
        mark_task_as_complete(sample_tasks, 0)
        captured = capsys.readouterr()
        assert "invalid" in captured.out.lower()

    def test_mark_task_returns_tasks(self, sample_tasks):
        result = mark_task_as_complete(sample_tasks, 1)
        assert isinstance(result, list)

    def test_mark_task_does_not_change_other_tasks(self, sample_tasks):
        mark_task_as_complete(sample_tasks, 1)
        assert sample_tasks[1]["status"] == "complete"  # was already complete
        assert sample_tasks[2]["status"] == "pending"


# ── view_pending_tasks ────────────────────────────────────────────────────────

class TestViewPendingTasks:
    def test_prints_only_pending_tasks(self, sample_tasks, capsys):
        view_pending_tasks(sample_tasks)
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 3" in captured.out
        assert "Task 2" not in captured.out  # Task 2 is complete

    def test_prints_nothing_when_no_pending(self, capsys):
        tasks = [{"title": "Done", "description": "Desc", "due_date": "2026-12-01", "status": "complete"}]
        view_pending_tasks(tasks)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_prints_nothing_for_empty_list(self, capsys):
        view_pending_tasks([])
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_output_contains_title_and_description(self, sample_tasks, capsys):
        view_pending_tasks(sample_tasks)
        captured = capsys.readouterr()
        assert "Desc 1" in captured.out


# ── calculate_progress ────────────────────────────────────────────────────────

class TestCalculateProgress:
    def test_empty_tasks_returns_zero(self):
        assert calculate_progress([]) == 0.0

    def test_all_pending_returns_zero(self, sample_tasks):
        tasks = [{"status": "pending"}, {"status": "pending"}]
        assert calculate_progress(tasks) == 0.0

    def test_all_complete_returns_100(self):
        tasks = [{"status": "complete"}, {"status": "complete"}]
        assert calculate_progress(tasks) == 100.0

    def test_half_complete_returns_50(self):
        tasks = [{"status": "complete"}, {"status": "pending"}]
        assert calculate_progress(tasks) == 50.0

    def test_mixed_tasks(self, sample_tasks):
        # sample_tasks has 1 complete out of 3
        result = calculate_progress(sample_tasks)
        assert result == pytest.approx(33.33, rel=0.01)

    def test_returns_float(self):
        tasks = [{"status": "complete"}]
        assert isinstance(calculate_progress(tasks), float)

    def test_completed_field_also_counts(self):
        tasks = [{"completed": True}, {"status": "pending"}]
        assert calculate_progress(tasks) == 50.0