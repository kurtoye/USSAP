// Toggle Sections
function showSection(sectionId) {
  document.querySelectorAll('section').forEach(section => {
    section.classList.add('hidden');
  });
  document.getElementById(sectionId).classList.remove('hidden');
}

// Submit Inquiry
document.getElementById('inquiry-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const studentId = document.getElementById('student-id').value;
  const message = document.getElementById('inquiry-message').value;

  const response = await fetch('/inquiries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_id: studentId, message })
  });

  const result = await response.json();
  alert(result.message || 'Inquiry submitted!');
});

// Submit Request
document.getElementById('request-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const studentId = document.getElementById('student-id-request').value;
  const type = document.getElementById('request-type').value;
  const details = document.getElementById('request-details').value;

  const response = await fetch('/requests', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_id: studentId, type, details })
  });

  const result = await response.json();
  alert(result.message || 'Request submitted!');
});

// Chatbot Interaction
document.getElementById('chatbot-send').addEventListener('click', async () => {
  const message = document.getElementById('chatbot-message').value;

  const response = await fetch('/chatbot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  });

  const result = await response.json();
  document.getElementById('chatbot-response').innerText = result.response || 'Error in chatbot!';
});
