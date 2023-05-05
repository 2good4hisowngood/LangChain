const fileUpload = document.getElementById('fileUpload');
const uploadBtn = document.getElementById('uploadBtn');
const queryInput = document.getElementById('queryInput');
const queryBtn = document.getElementById('queryBtn');
const answer = document.getElementById('answer');

uploadBtn.addEventListener('click', async () => {
    if (fileUpload.files.length === 0) {
        alert('Please select a file');
        return;
    }

    const file = fileUpload.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload file');
        }

        alert('File uploaded successfully');
    } catch (error) {
        alert(error.message);
    }
});

queryBtn.addEventListener('click', async () => {
    const query = queryInput.value;

    if (!query.trim()) {
        alert('Please enter a query');
        return;
    }

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: query })
        });

        if (!response.ok) {
            throw new Error('Failed to fetch answer');
        }

        const data = await response.json();
        answer.textContent = data.answer;
    } catch (error) {
        alert(error.message);
    }
});
