
from datetime import datetime
import functools
import json
import logging
from typing import Any, Callable, Optional
import pandas as pd

logger = logging.getLogger(__name__)


def report_logger(filename_or_func: Optional[Any] = None) -> Callable:
    """Декоратор для автоматического сохранения возвращаемого DataFrame в JSON-файл."""
    default_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> pd.DataFrame:
            result_df = func(*args, **kwargs)
            target_file = filename if 'filename' in locals() and isinstance(filename, str) else default_filename
            try:
                result_json = result_df.to_json(orient="records", force_ascii=False, indent=2)
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(result_json)
                logger.info(f"Отчет успешно сохранен в: {target_file}")
            except Exception as e:
                logger.error(f"Ошибка сохранения отчета в файл {target_file}: {e}")
            return result_df
        return wrapper

    if callable(filename_or_func):
        filename = default_filename
        return decorator(filename_or_func)
    else:
        filename = filename_or_func if filename_or_func else default_filename
        return decorator


@report_logger
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает траты по заданной категории за последние три месяца от опорной даты."""
    if transactions.empty:
        return pd.DataFrame()
    target_date = pd.to_datetime(date, dayfirst=True) if date else pd.Timestamp.now()
    start_date = target_date - pd.DateOffset(months=3)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= target_date) &
        (df["Категория"].str.lower() == category.lower()) &
        (df["Сумма операции"] < 0)
    ]
    return filtered_df


@report_logger("spending_by_weekday_report.json")
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    """Возвращает средние траты в каждый из дней недели за последние три месяца."""
    if transactions.empty:
        return pd.DataFrame()
    target_date = pd.to_datetime(date, dayfirst=True) if date else pd.Timestamp.now()
    start_date = target_date - pd.DateOffset(months=3)

    df = transactions.copy()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    filtered_df = df[
        (df["Дата операции"] >= start_date) &
        (df["Дата операции"] <= target_date) &
        (df["Сумма операции"] < 0)
    ].copy()

    if filtered_df.empty:
        return pd.DataFrame(columns=["День недели", "Средние траты"])

    filtered_df["Weekday_Num"] = filtered_df["Дата операции"].dt.weekday
    filtered_df["Сумма операции"] = filtered_df["Сумма операции"].abs()

    grouped = filtered_df.groupby("Weekday_Num")["Сумма операции"].mean().reset_index()
    weekday_names = {
        0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг",
        4: "Пятница", 5: "Суббота", 6: "Воскресенье"
    }
    grouped["День недели"] = grouped["Weekday_Num"].map(weekday_names)
    grouped = grouped.rename(columns={"Сумма операции": "Средние траты"}).round(2)
    return grouped[["День недели", "Средние траты"]].sort_index()
