import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2026-06-10T12:00:00.000000"},
        {"id": 2, "state": "PENDING",  "date": "2026-06-11T13:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2026-06-09T11:00:00.000000"},
        {"id": 4, "state": "EXECUTED"},                 # нет date
        {"id": 5, "state": "EXECUTED", "date": "bad"},  # невалидная строка
        {"id": 6, "state": "EXECUTED", "date": None},   # None
        {"id": 7, "state": "EXECUTED", "date": 12345},  # число
    ]

class TestFilterByState:
    def test_filter_executed(self, sample_data):
        result = filter_by_state(sample_data, "EXECUTED")
        # Было 5 → стало 6: у нас 6 элементов со state == EXECUTED
        assert len(result) == 6
        assert all(item["state"] == "EXECUTED" for item in result)

    def test_filter_pending(self, sample_data):
        result = filter_by_state(sample_data, "PENDING")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_nonexistent_state(self, sample_data):
        result = filter_by_state(sample_data, "UNKNOWN")
        assert result == []


class TestSortByDate:
    def test_sort_desc_with_invalid_dates(self, sample_data):
        result = sort_by_date(sample_data, reverse_order=True)
        ids = [item["id"] for item in result]
        # Валидные по убыванию: 2, 1, 3
        assert ids[:3] == [2, 1, 3]
        # Невалидные в конце (порядок между ними не важен)
        assert set(ids[3:]) == {4, 5, 6, 7}

    def test_sort_asc_with_invalid_dates(self, sample_data):
        result = sort_by_date(sample_data, reverse_order=False)
        ids = [item["id"] for item in result]
        # Валидные по возрастанию: 3, 1, 2
        assert ids[:3] == [3, 1, 2]
        assert set(ids[3:]) == {4, 5, 6, 7}

    def test_empty_list(self):
        assert sort_by_date([]) == []

    def test_all_invalid_dates_stay_at_end(self):
        data = [
            {"id": 10, "date": "bad"},
            {"id": 11},
            {"id": 12, "date": None},
            {"id": 13, "date": 999},
        ]
        result = sort_by_date(data, reverse_order=True)
        ids = [item["id"] for item in result]
        # Все невалидные → порядок сохраняется (stable)
        assert ids == [10, 11, 12, 13]

    def test_stable_sort_preserves_order_for_equal_dates(self):
        data = [
            {"id": 1, "date": "2026-01-01T00:00:00.000000"},
            {"id": 2, "date": "2026-01-01T00:00:00.000000"},
            {"id": 3, "date": "2026-01-01T00:00:00.000000"},
        ]
        result = sort_by_date(data, reverse_order=True)
        ids = [item["id"] for item in result]
        assert ids == [1, 2, 3]