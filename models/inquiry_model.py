class Inquiry:
<<<<<<< HEAD
    def __init__(self, student, message, status="Pending"):
        self.student = student
        self.message = message
        self.status = status

    def to_dict(self):
        return {
            "student": self.student,
            "message": self.message,
            "status": self.status,
=======
    def __init__(self, student_id, message, status="Pending", priority="Normal", created_at=None):
        self.student_id = student_id
        self.message = message
        self.status = status
        self.priority = priority
        self.created_at = created_at

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "message": self.message,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
>>>>>>> 473f8e2fcb236b6b92c1fba83b220230d6582a5b
        }
