const setupForm = document.getElementById('setup-form');
const statusDiv = document.getElementById('status-message');

setupForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const identity = setupForm.elements['identity'].value.trim();
  const roomName = setupForm.elements['roomName'].value.trim();
  const phone = setupForm.elements['phone'].value.trim();

  try {
    const response = await fetch('/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'identity': identity,
        'roomName': roomName,
        'phone': phone,
      })
    });

    await response.json();

    statusDiv.innerText = `Success! Office hours room: ${roomName} ✅`;
    setTimeout(() => { statusDiv.innerText = ''}, 5000);

  } catch (error) {
    console.log(error);
    statusDiv.innerText = `Error creating office hours room: ${error}`;
    setTimeout(() => { statusDiv.innerText = ''}, 5000);
  }
})
