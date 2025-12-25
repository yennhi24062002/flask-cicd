from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Lấy version từ environment variable hoặc dùng default
VERSION = os.getenv('APP_VERSION', '1.0.0')

@app.route('/')
def home():
    return jsonify({
        'message': 'Chào mừng đến với Flask CI/CD Demo!',
        'version': VERSION,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'version': VERSION
    }), 200

@app.route('/api/info')
def info():
    return jsonify({
        'app_name': 'Flask CI/CD Demo',
        'version': VERSION,
        'description': 'Demo application cho Jenkins CI/CD pipeline',
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Home page'},
            {'path': '/health', 'method': 'GET', 'description': 'Health check'},
            {'path': '/api/info', 'method': 'GET', 'description': 'Application info'}
        ]
    })

if __name__ == '__main__':
    # Chạy app trên port 5000, accessible từ bên ngoài container
    app.run(host='0.0.0.0', port=5000, debug=True)
