import pytest
from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00.000000"},
        {"id": 2, "state": "PENDING", "date": "2024-01-02T11:00:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-03T12:00:00.000000"},
        {"id": 4, "state": "EXECUTED"},  # нет даты
        {"id": 5, "state": "EXECUTED", "date": "invalid-date"},
        {"id": 6, "state": "EXECUTED", "date": None},
    ]


@pytest.mark.parametrize(
    "state,expected_count",
    [
        ("EXECUTED", 5),
        ("PENDING", 1),
        ("UNKNOWN", 0),
    ],
)
def test_filter_by_state(sample_data, state, expected_count):
    result = filter_by_state(sample_data, state)
    assert len(result) == expected_count
    assert all(item.get("state") == state for item in result)


def test_sort_by_date_desc(sample_data):
    # Ожидаем: сначала валидные даты по убыванию, потом невалидные
    result = sort_by_date(sample_data, reverse_order=True)

    # Первые 3 — валидные даты, идут по убыванию
    assert result[0]["id"] == 3
    assert result[1]["id"] == 2
    assert result[2]["id"] == 1

    # Остальные — невалидные/отсутствующие даты (порядок не важен, но они в конце)
    invalid_ids = {item["id"] for item in result[3:]}
    assert invalid_ids == {4, 5, 6}


def test_sort_by_date_asc(sample_data):
    result = sort_by_date(sample_data, reverse_order=False)

    # Валидные по возрастанию
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    assert result[2]["id"] == 3

    invalid_ids = {item["id"] for item in result[3:]}
    assert invalid_ids == {4, 5, 6}