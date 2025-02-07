import os
import requests
from flask import Flask, jsonify
import time


app = Flask(__name__)

SERVICE_B_URL = "http://localhost:10000"  # Envoy proxy for Service B

@app.route('/')
def home():
    return "Hello from Service A!"


@app.route('/delay')
def delay():
    time.sleep(60)
    return "Delay response from service A"


@app.route('/callDelayEndpoint', methods=['GET'])
def call_delayed_endpoint():
    try:
        # Forward the request to Service B
        response = requests.get(f"http://localhost:12000/delay")
        return jsonify(message="Request to Service succeeded", serviceB_response=response.text), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify(message="Request to Service B failed", error=str(e)), 500

@app.route('/callDelayEndpointWithTimeout', methods=['GET'])
def call_delayed_endpoint_with_timeout():
    try:
        # Forward the request to Service B
        response = requests.get(f"http://localhost:12000/delay", timeout=5)
        return jsonify(message="Request to Service succeeded", serviceB_response=response.text), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify(message="Request to Service B failed", error=str(e)), 500

@app.route('/serviceB', methods=['GET'])
def call_serviceB():
    try:
        # Forward the request to Service B
        response = requests.get(f"{SERVICE_B_URL}/serviceB", timeout=5)
        return jsonify(message="Request to Service B succeeded", serviceB_response=response.text), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify(message="Request to Service B failed", error=str(e)), 500

@app.route('/serviceC', methods=['GET'])
def call_serviceC():
    try:
        # Forward the request to Service B
        response = requests.get(f"{SERVICE_B_URL}/serviceC", timeout=5)
        return jsonify(message="Request to Service B succeeded", serviceB_response=response.text), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify(message="Request to Service B failed", error=str(e)), 500

@app.route('/healthcheck', methods=['GET'])
def call_service_healthcheck():
    try:
        response = requests.get(f"{SERVICE_B_URL}/healthcheck", timeout=5)
        return jsonify(message="Request to  healthcheck succeeded", serviceB_response=response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify(message="Request to healthcheck failed", error=str(e)), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)  # Service A listens on port


