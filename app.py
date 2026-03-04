import logging
import sys
import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Configure structured logging to stdout
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger("test-log-app")

# Simulate different log levels
ACTIONS = [
    ("Processing request", logging.INFO),
    ("User logged in", logging.INFO),
    ("File uploaded successfully", logging.INFO),
    ("Slow response detected", logging.WARNING),
    ("Retry attempt", logging.WARNING),
    ("Low memory warning", logging.WARNING),
    ("Database connection failed", logging.ERROR),
    ("Timeout error", logging.ERROR),
    ("Invalid input received", logging.ERROR),
]

@app.route("/")
def home():
    logger.info("Home endpoint hit")
    return jsonify({"status": "running", "message": "Test Log App is alive!"})

@app.route("/generate")
def generate_logs():
    """Generate random logs"""
    count = 10
    for i in range(count):
        message, level = random.choice(ACTIONS)
        logger.log(level, f"{message} - request #{i+1}")
        time.sleep(0.1)
    return jsonify({"status": "ok", "logs_generated": count})

@app.route("/error")
def trigger_error():
    """Trigger an error log"""
    logger.error("Critical error triggered manually!")
    return jsonify({"status": "error triggered"}), 500

@app.route("/health")
def health():
    logger.info("Health check passed")
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    logger.info("Test Log App starting up...")
    app.run(host="0.0.0.0", port=5001)