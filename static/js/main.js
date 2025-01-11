let editor = null;
let platforms = null;

document.addEventListener('DOMContentLoaded', async function() {
    // Initialize the JSON editor
    const container = document.getElementById('jsoneditor');
    const options = {
        mode: 'view',
        modes: ['view', 'form', 'code'],
        sortObjectKeys: true,
    };
    editor = new JSONEditor(container, options);
    
    // Load platforms for the dropdown
    await loadPlatforms();
});

async function loadPlatforms() {
    try {
        const response = await fetch('/api/platforms');
        platforms = await response.json();
        
        // Populate platform select
        const select = document.getElementById('platformSelect');
        platforms.forEach(platform => {
            if (platform.supported_urls) {  // Only add platforms with URL patterns
                const option = document.createElement('option');
                option.value = platform.name;
                option.textContent = platform.description || platform.name;
                select.appendChild(option);
            }
        });
    } catch (error) {
        console.error('Error loading platforms:', error);
    }
}

function updateUrlFormat() {
    const platformName = document.getElementById('platformSelect').value;
    const helpText = document.getElementById('urlFormatHelp');
    
    if (!platformName) {
        helpText.textContent = 'Select a platform to see URL format';
        return;
    }
    
    const platform = platforms.find(p => p.name === platformName);
    if (platform) {
        let helpString = 'URL Format: ';
        if (platform.example_urls && platform.example_urls.length > 0) {
            helpString += `\nExample: ${platform.example_urls[0]}`;
        }
        helpText.textContent = helpString;
    }
}

async function exploreGuidedUrl() {
    const url = document.getElementById('guidedUrlInput').value;
    if (!url) {
        alert('Please enter a URL');
        return;
    }
    
    await exploreUrlCommon(url);
}

async function exploreUrl() {
    const url = document.getElementById('universalUrlInput').value;
    if (!url) {
        alert('Please enter a URL');
        return;
    }
    
    await exploreUrlCommon(url);
}

async function exploreUrlCommon(url) {
    try {
        const response = await fetch('/api/explore', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url }),
        });
        const data = await response.json();
        editor.set(JSON.parse(data.metadata || data));
    } catch (error) {
        console.error('Error:', error);
        editor.set({ error: 'Error exploring URL', details: error.message });
    }
} 