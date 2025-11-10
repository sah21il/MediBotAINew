from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class ObservationMessage(BaseModel):
    schema_version: str = Field(default="1.0")
    message_id: str
    patient_id: str
    type: str
    timestamp: datetime
    payload: Dict[str, Any]
    provenance: Dict[str, Any]
