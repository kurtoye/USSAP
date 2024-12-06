const API_BASE_URL = "http://127.0.0.1:8080"; // Update with your backend URL if different

// Submit Inquiry
document.getElementById("inquiry-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const studentName = document.getElementById("student-name").value;
  const inquiryMessage = document.getElementById("inquiry-message").value;

  try {
    const response = await fetch(`${API_BASE_URL}/inquiries/submit`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        student: studentName,
        message: inquiryMessage,
      }),
    });
    const data = await response.json();
    document.getElementById("inquiry-response").textContent = data.status
      ? `Inquiry Submitted: ${data.status}`
      : `Error: ${data.error}`;
  } catch (error) {
    document.getElementById("inquiry-response").textContent = `Error: ${error.message}`;
  }
});

// Load All Requests
document.getElementById("view-requests").addEventListener("click", async () => {
  const requestsList = document.getElementById("requests-list");
  requestsList.innerHTML = ""; // Clear existing list

  try {
    const response = await fetch(`${API_BASE_URL}/requests`, {
      method: "GET",
    });
    const data = await response.json();

    if (data.length === 0) {
      requestsList.innerHTML = "<li>No requests found.</li>";
    } else {
      data.forEach((request) => {
        const listItem = document.createElement("li");
        listItem.textContent = `Request ID: ${request.id}, Student: ${request.name}, Status: ${request.status}`;
        requestsList.appendChild(listItem);
      });
    }
  } catch (error) {
    const errorItem = document.createElement("li");
    errorItem.textContent = `Error: ${error.message}`;
    requestsList.appendChild(errorItem);
  }
});
