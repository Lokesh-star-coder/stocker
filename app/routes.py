from flask import Blueprint, jsonify
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': 'Book Exchange API is running'
    })

@main.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'database': 'connected' if db.engine else 'disconnected'
    })
