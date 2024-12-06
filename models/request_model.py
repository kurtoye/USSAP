class Request:
    def __init__(self, student_id, type, details, status="Pending"):
        self.student_id = student_id
        self.type = type
        self.details = details
        self.status = status

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "type": self.type,
            "details": self.details,
            "status": self.status,
        }
