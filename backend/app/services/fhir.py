def convert_to_fhir(parsed_data):
    document_type = parsed_data.get("document_type", "unknown")
    
    if document_type == "prescription":
        fhir_entry = {
            "resourceType": "MedicationRequest",
            "id": parsed_data.get("id", "unknown"),
            "subject": {"reference": f"Patient/{parsed_data.get('patient_id', 'unknown')}"},
            "medicationCodeableConcept": {"text": parsed_data.get("medication")},
            "dosageInstruction": [{"text": parsed_data.get("dosage")}]
        }
    elif document_type == "diagnosis":
        fhir_entry = {
            "resourceType": "Condition",
            "id": parsed_data.get("id", "unknown"),
            "subject": {"reference": f"Patient/{parsed_data.get('patient_id', 'unknown')}"},
            "code": {"text": parsed_data.get("diagnosis")},
            "onsetDateTime": parsed_data.get("date")
        }
    elif document_type == "test_results":
        fhir_entry = {
            "resourceType": "Observation",
            "id": parsed_data.get("id", "unknown"),
            "subject": {"reference": f"Patient/{parsed_data.get('patient_id', 'unknown')}"},
            "code": {"text": parsed_data.get("test_name")},
            "valueString": parsed_data.get("result"),
            "effectiveDateTime": parsed_data.get("date")
        }
    else:
        fhir_entry = {
            "resourceType": "DocumentReference",
            "id": parsed_data.get("id", "unknown"),
            "subject": {"reference": f"Patient/{parsed_data.get('patient_id', 'unknown')}"},
            "description": "Unclassified document",
            "content": [{"attachment": {"data": parsed_data.get("raw_text")}}]
        }
    
    return fhir_entry