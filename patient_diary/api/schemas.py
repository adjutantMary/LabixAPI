from pydantic import BaseModel
from typing import Optional, Union


class AnalyseData(BaseModel):
    marker: str
    value: float
    normal: str
    unitOfMeasurement: str
    problem: dict[str, list[str]]

class PatientData(BaseModel):
    # fio: str
    snils: str
    analyzes: list[AnalyseData]

    class Config:
        json_schema_extra = {
            "example": {
                # "fio": "Иванов Иван Иванович",
                "snils": "11142234",
                "analyzes": [
                    {
                        "marker": "СРБ",
                        "value": 12.5,
                        "normal": "0-6",
                        "unitOfMeasurement": "ммHg",
                        "problem": {
                            "system": "Иммунная система",
                            "problems": ["Аллергическая сенсибилизация", "Воспалительный ответ"]}
                    },
                ],
            }
        }
