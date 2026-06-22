def filter_by_states(data_list, states=None):
    """Фильтрует данные по нескольким статусам."""
    if states is None:
        states = ["EXECUTED", "CANCELED"]
    result = {}
    for state in states:
        result[state] = [item for item in data_list if item.get("state") == state]
    return result


def sort_by_date(data_list, reverse=True):
    """Сортирует данные по дате."""
    return sorted(data_list, key=lambda item: item.get("date", ""), reverse=reverse)
