from flask import Flask, render_template, request, jsonify
from platform_explorer import PlatformExplorer
from instagram_explorer import explore_instagram_profile

app = Flask(__name__)
explorer = PlatformExplorer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    platforms = explorer.get_supported_platforms()
    return jsonify(platforms)

@app.route('/api/explore', methods=['POST'])
def explore_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    metadata = explorer.explore_platform_metadata(url)
    return jsonify({'metadata': metadata})

@app.route('/api/instagram', methods=['POST'])
def explore_instagram():
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    metadata = explore_instagram_profile(username)
    return jsonify({'metadata': metadata})

if __name__ == '__main__':
    app.run(debug=True, port=5002) 