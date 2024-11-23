import json
import os
import pandas as pd
from pathlib import Path
from ninja import NinjaAPI
from .schemas import AnalyseData, PatientData
from .utils import process_patient_data


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patient_diary.settings')
api = NinjaAPI()

DATA_STORAGE_FILE = Path("./data")

@api.post("/add-diary-record/{snils}")
def post_patient_snils(request, snils: str):
    file_path = DATA_STORAGE_FILE / f"{snils}.json"
    if file_path.exists():
        print("File exists")
        return file_path
    else:
        return {"error": "Patient not found"}, 404


@api.get("/get-patient-data/{snils}")
def get_patient_data(request, snils: str):
    file_path = DATA_STORAGE_FILE / f"{snils}.json"
    if not file_path.exists():
        return {"error": "Patient not found"}, 404
    
    patient_data = process_patient_data(file_path)
    
    return {
        "snils": patient_data.snils,
        "analyzes": [
            {
                "marker": analyze.marker,
                "value": analyze.value,
                "normal": analyze.normal,
                "unitOfMeasurement": analyze.unitOfMeasurement,
                "problem": analyze.problem
            }
            for analyze in patient_data.analyzes
        ]
    }

    # """Добавить запись в дневник пациента"""

    # file_path = DATA_STORAGE_FILE / f"{snils}.json"

    # if file_path.exists():
    #     with file_path.open("r") as f:
    #         content = f.read()
    #         if content.strip():
    #             data = json.loads(content)
    #         else:
    #             data = {"diary": []}
    # else:
    #     data = {"diary": []}

    # marker_ranges = json.load(open(MARKER_RANGES_PATH, 'r'))
    # data = {
    #     "Пульс": record.heart_rate,
    #     "Частота дыхания": record.respiration_rate,
    #     "Диастолическое давление": record.distolic_pressure,
    #     "Систолическое давление": record.systolic_pressure,
    #     "Сатурация": record.saturation,
    # }
    # res = check(record.model_dump(), marker_ranges)
    # output = extract_conditions(res, pd.read_excel(FILTERED_DATA_PATH))
    # # merged_df = merge_data(data["diary"][-1], pd.read_excel(FILTERED_DATA_PATH), res)

    # record.state = ", ".join(output.values())

    # data["diary"].append(record.model_dump())

    # # Записываем обновленные данные
    # with file_path.open("w") as f:
    #     json.dump(data, f, indent=4)

    # print(f"Запись успешно добавлена в дневник пациента с СНИЛС: {snils}")
    # return {"message": "Запись успешно добавлена"}


@api.get("/get-patient-data/{snils}")
def get_patient_path(request, snils: str) -> PatientData:
    """Получить данные о пациенте"""

    file_path = DATA_STORAGE_FILE / f"{snils}.json"

    if file_path.exists():
        with open(file_path, "r") as f:
            data = json.load(f)
            return PatientData(**data)
    else:
        return {"error": "Patient not found"}, 404
    pass
