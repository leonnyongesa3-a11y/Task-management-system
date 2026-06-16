import pytest
from task_manager.validation import validate_task_title, validate_task_description, validate_due_date, validate_priority


class TestValidateTaskTitle:
    def test_valid_title(self):
        assert validate_task_title("Valid Title") is True

    def test_empty_title(self):
        with pytest.raises(ValueError):
            validate_task_title("")

    def test_whitespace_only_title(self):
        with pytest.raises(ValueError):
            validate_task_title("   ")


class TestValidateTaskDescription:
    def test_valid_description(self):
        assert validate_task_description("Valid description") is True

    def test_empty_description(self):
        with pytest.raises(ValueError):
            validate_task_description("")

    def test_too_long_description(self):
        with pytest.raises(ValueError):
            validate_task_description("x" * 501)


class TestValidateDueDate:
    def test_valid_date(self):
        assert validate_due_date("2026-12-01") is True

    def test_empty_date(self):
        with pytest.raises(ValueError):
            validate_due_date("")

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            validate_due_date("not-a-date")


class TestValidatePriority:
    def test_valid_text_priority_low(self):
        assert validate_priority("low") is True

    def test_valid_text_priority_medium(self):
        assert validate_priority("medium") is True

    def test_valid_text_priority_high(self):
        assert validate_priority("high") is True

    def test_valid_numeric_priority(self):
        assert validate_priority(3) is True

    def test_valid_numeric_priority_range(self):
        for p in [1, 2, 3, 4, 5]:
            assert validate_priority(p) is True

    def test_invalid_text_priority(self):
        with pytest.raises(ValueError):
            validate_priority("urgent")

    def test_invalid_numeric_priority_low(self):
        with pytest.raises(ValueError):
            validate_priority(0)

    def test_invalid_numeric_priority_high(self):
        with pytest.raises(ValueError):
            validate_priority(6)

    def test_invalid_priority_non_numeric(self):
        with pytest.raises(ValueError):
            validate_priority("invalid")