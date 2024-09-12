document.getElementById('generatebutton').addEventListener('click', async () => {
            
const videoLink = document.getElementById('streamlink').value;
const scriptContent = document.getElementById('script-content');
const summaryContent = document.getElementById('summary-content')

// Get cookie from django:
function getCookie(name) {
var cookieValue = null;
if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // If the cookie string begins with the name we want.
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}

// Function to validate YouTube URLs
function isValidYouTubeURL(url) {
    const regex = /^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$/;
    return regex.test(url);
}

if(videoLink) {
    document.getElementById('loading-ring').style.display = 'block';

    // Validate YouTube link
    if (!isValidYouTubeURL(videoLink)) {
        alert("Please enter a valid YouTube link.");
        return;
    }
    
    // Clear previous content
    scriptContent.innerHTML = '';
    summaryContent.innerHTML = '';

    const endpointUrl = '/generate';
    
    try {
        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {                
                'X-CSRFToken': getCookie('csrftoken'),
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