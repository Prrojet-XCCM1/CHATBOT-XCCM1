import os
import sys

from flask import jsonify, request
from app import create_app
from app.utils.logger import logger

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = create_app()

@app.before_request
def log_request_info():
    """Logger les informations de requête"""
    logger.info("Request received", extra={
        "method": request.method,
        "path": request.path,
        "remote_addr": request.remote_addr
    })

@app.errorhandler(404)
def not_found_error(error):
    logger.warning("Route not found", extra={"path": request.path})
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error("Internal server error", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Education Multi-Agent API on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)