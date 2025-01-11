from yt_dlp import YoutubeDL
from yt_dlp.extractor import list_extractors
import json
import re

class PlatformExplorer:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
    
    def get_supported_platforms(self):
        """Get all supported platforms/extractors"""
        extractors = list_extractors()
        platforms = []
        
        for e in extractors:
            if e._WORKING:  # Only include working extractors
                platforms.append({
                    'name': e.IE_NAME,
                    'description': e.IE_DESC,
                    'working': e._WORKING,
                    'supported_urls': e._VALID_URL_RE.pattern if hasattr(e, '_VALID_URL_RE') else None,
                    'example_urls': getattr(e, '_EXAMPLES', [])  # Add example URLs if available
                })
        
        return platforms

    def explore_platform_metadata(self, url):
        """
        Explore available metadata for a specific URL
        Example URLs:
        - YouTube: https://www.youtube.com/watch?v=VIDEO_ID
        - Instagram: https://www.instagram.com/p/POST_ID/
        - TikTok: https://www.tiktok.com/@username/video/VIDEO_ID
        """
        if not url:
            return json.dumps({"error": "URL is required"})
            
        try:
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return json.dumps(info, indent=2)
        except Exception as e:
            return json.dumps({
                "error": str(e),
                "message": "Make sure the URL is correct and accessible",
                "url_provided": url
            }, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Explore YT-DLP supported platforms and metadata')
    parser.add_argument('--list-platforms', action='store_true', help='List all supported platforms')
    parser.add_argument('--url', type=str, help='URL to explore metadata')
    
    args = parser.parse_args()
    explorer = PlatformExplorer()
    
    if args.list_platforms:
        platforms = explorer.get_supported_platforms()
        print(json.dumps(platforms, indent=2))
    
    if args.url:
        metadata = explorer.explore_platform_metadata(args.url)
        print(metadata)

if __name__ == "__main__":
    main() 