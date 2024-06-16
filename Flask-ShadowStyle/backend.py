import psutil
import GPUtil
import json
import socket
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for all domains on all routes

def get_system_info():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # RAM usage
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    
    # Disk usage
    disk = psutil.disk_usage('/')
    disk_total = disk.total // (2**30)  # Convert bytes to GB
    disk_used = disk.used // (2**30)
    disk_free = disk.free // (2**30)
    disk_usage = disk.percent
    
    # GPU usage
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            'gpu_name': gpu.name,
            'gpu_load': gpu.load * 100,
            'gpu_free_memory': gpu.memoryFree,
            'gpu_used_memory': gpu.memoryUsed,
            'gpu_total_memory': gpu.memoryTotal,
            'gpu_temperature': gpu.temperature
        })
    
    # CPU temperature
    cpu_temp = None
    try:
        if hasattr(psutil, 'sensors_temperatures'):
            temp = psutil.sensors_temperatures()
            if 'coretemp' in temp:
                cpu_temp = temp['coretemp'][0].current
    except Exception as e:
        cpu_temp = 'N/A'
    
    # Private IP
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
    
    # Public IP
    public_ip = requests.get('https://api.ipify.org').text
    
    return {
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'disk_total': disk_total,
        'disk_used': disk_used,
        'disk_free': disk_free,
        'disk_usage': disk_usage,
        'gpu_info': gpu_info,
        'cpu_temp': cpu_temp,
        'private_ip': private_ip,
        'public_ip': public_ip
    }

@app.route('/system_info', methods=['GET'])
def system_info():
    info = get_system_info()
    return jsonify(info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
