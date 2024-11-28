<<<<<<< HEAD
def validate_request_data(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
=======
def validate_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        raise ValueError(f"Missing fields: {', '.join(missing_fields)}")
>>>>>>> 473f8e2fcb236b6b92c1fba83b220230d6582a5b
