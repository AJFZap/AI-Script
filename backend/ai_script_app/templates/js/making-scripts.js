
CSRF_TOKEN = '{{ csrf_token }}'

document.getElementById('generatebutton').addEventListener('click', async () => {
            
const videoLink = document.getElementById('streamlink').value;
const scriptContent = document.getElementById('script-content');
const summaryContent = document.getElementById('summary-content')

if(videoLink) {
    document.getElementById('loading-ring').style.display = 'block';
    
    // Clear previous content
    scriptContent.innerHTML = '';
    summaryContent.innerHTML = '';

    const endpointUrl = '/generate';
    
    try {
        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': CSRF_TOKEN,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ link: videoLink })
        });

        const data = await response.json();

        // Check if the response contains an error
        if (data['error']) {
            // If error exists, throw an error
            throw new Error(data['error']);
        }

        // Show the results!
        scriptContent.innerHTML = data['script-content'];
        summaryContent.innerHTML = data['summary'];
        document.getElementById('script-gen').style.display = 'block';

    } catch (error) {
        document.getElementById('script-gen').style.display = 'none';
        console.error('', error);
        alert('Error occurred: ' + error.message);
        
    }
    document.getElementById('loading-ring').style.display = 'none';
} else {
    alert("Please enter a Video link.");
}
});