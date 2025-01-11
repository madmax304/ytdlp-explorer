from yt_dlp import YoutubeDL
import json

def explore_instagram_profile(username):
    """
    Explore Instagram profile metadata
    Args:
        username (str): Instagram username without @ symbol
                       Example: 'instagram' for https://www.instagram.com/instagram/
    """
    if not username:
        return json.dumps({"error": "Username is required"})
        
    # Remove @ symbol if provided
    username = username.lstrip('@')
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    url = f"https://www.instagram.com/{username}/"
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return json.dumps(info, indent=2)
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "message": "Make sure the username exists and the profile is public",
            "username_provided": username,
            "url_attempted": url
        }, indent=2)

# Example usage
if __name__ == "__main__":
    username = "example_username"
    result = explore_instagram_profile(username)
    print(result) 