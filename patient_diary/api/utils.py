import json
import pandas as pd
from pathlib import Path
from .schemas import AnalyseData, PatientData
from .analyse import process_files


DATA_STORAGE_FILE = Path("./data")
FILTERED_DATA_PATH = Path("./data/filtered_data_with_sex.xlsx")
MARKER_RANGES_PATH = Path("./data/marker_ranges.json")

def process_patient_data(file_path: str) -> PatientData:
    # with open(file_path, "r") as f:
    #     patient = json.load(f)

    filtered_data_path = FILTERED_DATA_PATH
    marker_ranges_path = MARKER_RANGES_PATH

    output, merged_df = process_files(file_path, filtered_data_path, marker_ranges_path)

    analyzes = []
    for index, row in merged_df.iterrows():
        problem = {}
        if row["Маркеры"] in output:
            system_name = list(output.keys())[0]
            problem = {"system": system_name, "problems": [output[system_name]]}
        analyze = AnalyseData(
            marker=row["Маркеры"],
            value=row["Значение"],
            normal=row["Норма"],
            unitOfMeasurement=row["Ед.изм."],
            problem=problem
        )
        analyzes.append(analyze)

    patient_data = PatientData(
        snils=file_path.stem,
        analyzes=analyzes
    )

    return patient_data

snils = "11142234"
path = DATA_STORAGE_FILE / f"{snils}.json"

print(process_patient_data(path))
