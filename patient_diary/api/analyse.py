# client_1 = {
#     "Тромбоциты": 270,
#     "Лейкоциты": 13,
#     "Гемоглобин (Муж)": 152,
#     "Гематокрит": 40,
#     "Эритроциты": 15,
#     "Палочкоядерные нейтрофилы": 3.8,
#     "Сегментоядерные нейтрофилы": 60,
#     "Эозинофилы": 2.2,
#     "Среднее содержание гемоглобина в эритроците, MCH": 30,
#     "Средняя концентрация гемоглобина в эритроците, MCHC (Муж)": 340,
#     "Средний объем эритроцита, MCV": 86,
#     "Базофилы": 0.5,
#     "Моноциты": 5,
#     "Лимфоциты": 26,
#     "СРБ": 2.9,
#     "Глюкоза": 5.3,
#     "Креатинин (Муж)": 87,
#     "Фибриноген": 3.3,
#     "СОЭ (Муж)": 20,
#     "pH (артериальная кровь)": 7.25,
#     "рСО2 (артериальная кровь)": 55,
#     "рО2 (артериальная кровь)": 72,
#     "HCO3- (стандартный)": 18,
#     "Кальций ионизированный (Ca++)": 1.1,
#     "Натрий": 136,
#     "Калий": 4.8,
# }

# %% [code]
from pathlib import Path
import pandas as pd
import json
import numpy as np


# Функция для проверки значений и отклонений
def check(data, marker_ranges):
    result = {}
    for marker, value in data.items():
        if marker in marker_ranges:
            low, up = marker_ranges[marker]
            if low <= value <= up:
                result[marker] = (0, "=")
            else:
                deviation = "+" if value > up else "-"
                result[marker] = (1, deviation)
    return result


# Функция для извлечения состояний на основе отклонений
def extract_conditions(res, filtered_df):
    output = {}

    for marker, (status, deviation) in res.items():
        if status == 1:
            condition_rows = filtered_df[filtered_df["Маркеры"] == marker]

            for _, condition_row in condition_rows.iterrows():
                system = condition_row["Системы"]
                condition = condition_row["Состояния"]
                expected_deviation = condition_row["Отклонения"]

                if deviation == expected_deviation:
                    if system not in output:
                        output[system] = set()
                    output[system].add(condition)
    for system in output:
        output[system] = list(output[system])

    return output

def merge_data(data, filtered_df, res):
    filtered_df = filtered_df[filtered_df["Маркеры"].isin(data.keys())].copy()

    filtered_df["Значение"] = filtered_df["Маркеры"].map(data)

    def update_deviation(row):
        marker = row["Маркеры"]
        if marker in res:
            status, deviation = res[marker]
            if status == 0:
                return np.nan
            else:
                if row["Отклонения"] == deviation:
                    return deviation
                else:
                    return np.nan
        return np.nan

    filtered_df["Отклонение"] = filtered_df.apply(update_deviation, axis=1)
    filtered_df = filtered_df[["Маркеры", "Значение", "Норма", "Ед.изм.", "Отклонение"]]

    return filtered_df


# Основная функция для обработки
def process_files(data_path, filtered_data_path, marker_ranges_path):
    with open(data_path, "r") as f:
        data = json.load(f)
    # data = client_1
    # Чтение данных
    filtered_df = pd.read_excel(
        filtered_data_path
    )  # Читаем Excel файл с таблицей анализов из папки /data

    with open(marker_ranges_path, "r") as f:
        marker_ranges = json.load(
            f
        )  # Чтение JSON файла с диапазонами маркеров также из папки /data

    # Обработка данных
    res = check(data, marker_ranges)
    output = extract_conditions(res, filtered_df)
    merged_df = merge_data(data, filtered_df, res)

    # Возвращаем результаты
    return output, merged_df

DATA_STORAGE_FILE = Path("./data")
FILTERED_DATA_PATH = Path("./data/filtered_data_with_sex.xlsx")
MARKER_RANGES_PATH = Path("./data/marker_ranges.json")

# Пример использования
# filtered_data_path = FILTERED_DATA_PATH
# marker_ranges_path = MARKER_RANGES_PATH

# output, merged_data = process_files(client_1, filtered_data_path, marker_ranges_path)

# print("Output:", output)
