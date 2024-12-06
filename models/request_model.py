class Request:
    def __init__(self, student_id, name, request, status="Pending"):
        self.student_id = student_id
        self.name = name
        self.request = request
        self.status = status

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "request": self.request,
            "status": self.status,
        }
