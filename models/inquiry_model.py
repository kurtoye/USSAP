class Inquiry:
    def __init__(self, student, message, status="Pending"):
        self.student = student
        self.message = message
        self.status = status

    def to_dict(self):
        return {
            "student": self.student,
            "message": self.message,
            "status": self.status,
        }
