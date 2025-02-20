from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date, datetime

# Users Table (Personal Profile)
class User(BaseModel):
    user_id: Optional[int] = None
    first_name: constr(max_length=50)
    last_name: constr(max_length=50)
    date_of_birth: date
    # gender: constr(max_length=10, regex="^(Male|Female|Other)$")
    phone: Optional[constr(max_length=20)] = None
    email: EmailStr
    address: Optional[str] = None
    created_at: Optional[datetime] = None

# Medical Records Table (Stores All Uploaded Documents)
class MedicalRecord(BaseModel):
    record_id: Optional[int] = None
    user_id: int
    #record_type: constr(max_length=50, regex="^(Diagnosis|Prescription|Lab Report|Imaging|Consultation|Other)$")
    description: Optional[str] = None
    document_url: Optional[constr(max_length=255)] = None
    uploaded_at: Optional[datetime] = None

# Diagnoses Table (Tracks Medical Conditions)
class Diagnosis(BaseModel):
    diagnosis_id: Optional[int] = None
    user_id: int
    doctor_name: constr(max_length=100)
    condition: constr(max_length=255)
    severity: Optional[constr(max_length=50)] = None
    diagnosis_date: date
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

# Prescriptions Table (Tracks Medications)
class Prescription(BaseModel):
    prescription_id: Optional[int] = None
    user_id: int
    doctor_name: constr(max_length=100)
    medication: constr(max_length=255)
    dosage: constr(max_length=50)
    frequency: constr(max_length=50)
    start_date: date
    end_date: Optional[date] = None
    instructions: Optional[str] = None
    created_at: Optional[datetime] = None

# Lab Results Table (Stores Test Results)
class LabResult(BaseModel):
    lab_id: Optional[int] = None
    user_id: int
    test_name: constr(max_length=255)
    result_value: Optional[str] = None
    reference_range: Optional[constr(max_length=100)] = None
    test_date: date
    notes: Optional[str] = None
    document_url: Optional[constr(max_length=255)] = None
    created_at: Optional[datetime] = None

# Vaccination Records Table
class Vaccination(BaseModel):
    vaccination_id: Optional[int] = None
    user_id: int
    vaccine_name: constr(max_length=255)
    dose: Optional[constr(max_length=50)] = None
    vaccination_date: date
    notes: Optional[str] = None
    created_at: Optional[datetime] = None

# Example Query Models
class QueryResponse(BaseModel):
    answer: str
    document_link: Optional[str] = None

class QueryRequest(BaseModel):
    query: str

class ParagraphResponse(BaseModel):
    doc_id: str
    paragraph_id: int
    text: str



