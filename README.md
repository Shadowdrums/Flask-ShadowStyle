# Flask-ShadowStyle
Flask-ShadowStyle, proof of concept for a local flask server

# Flask-ShadowStyle

**Flask-ShadowStyle** is a sleek and modern web application designed to display live hardware information. Utilizing the power of Flask on the backend and a clean HTML interface, it provides real-time insights into your system’s performance metrics.

## 🚀 Features

- **Real-Time CPU Usage**: Monitor your CPU load in real-time.
- **Memory Utilization**: Keep track of your RAM usage.
- **Disk Space Management**: View your total, used, and free disk space.
- **CPU Temperature**: Get readings of your CPU temperature.
- **GPU Details**: See GPU name, load, and temperature.
- **IP Addresses**: Display both private and public IP addresses.
- **Quick Redirect**: One-click button to redirect to your specified URL.

## 🛠️ Requirements

- Python 3.x
- Flask
- Flask-CORS
- psutil
- GPUtil
- requests

## 📦 Installation

1. **Clone the Repository**
    ```sh
    git clone https://github.com/yourusername/Flask-ShadowStyle.git
    cd Flask-ShadowStyle
    ```

2. **Install Dependencies**
    ```sh
    pip install flask flask-cors psutil GPUtil requests
    ```

## ▶️ Usage

1. **Run the Application**
    ```sh
    python main.py
    ```

## 📁 Project Structure

```plaintext
Flask-ShadowStyle/
├── backend.py       # Python script to gather and serve system information
├── main.py       #builds and runs HTML file and backend to display the system information
└── README.md        # This README file
```

🔧 Backend Script (backend.py)
This script uses Flask to create a web server that serves system information at the /system_info endpoint. It gathers information using psutil and GPUtil libraries.

Example Backend Code:

import psutil
import GPUtil
import socket
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    disk = psutil.disk_usage('/')
    disk_total = disk.total // (2**30)
    disk_used = disk.used // (2**30)
    disk_free = disk.free // (2**30)
    disk_usage = disk.percent
    gpus = GPUtil.getGPUs()
    gpu_info = [{'gpu_name': gpu.name, 'gpu_load': gpu.load * 100, 'gpu_temperature': gpu.temperature} for gpu in gpus]
    cpu_temp = None
    try:
        temp = psutil.sensors_temperatures()
        cpu_temp = temp['coretemp'][0].current if 'coretemp' in temp else None
    except:
        pass
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
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
    return jsonify(get_system_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

🌐 Frontend (index.html)
The HTML file fetches system information from the backend and displays it in a clean, user-friendly format. It also includes a button that redirects to http://www.shadowdrums.com when clicked.

Example Frontend Code:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Info</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .info { margin: 20px; }
        .info div { margin-bottom: 10px; }
    </style>
    <script type="text/javascript">
        function redirectToPage() {
            window.location.href = 'http://www.shadowdrums.com';
        }

        async function fetchSystemInfo() {
            try {
                const response = await fetch('http://127.0.0.1:5000/system_info');
                const data = await response.json();
                document.getElementById('cpu_usage').innerText = data.cpu_usage;
                document.getElementById('ram_usage').innerText = data.ram_usage;
                document.getElementById('disk_total').innerText = data.disk_total;
                document.getElementById('disk_used').innerText = data.disk_used;
                document.getElementById('disk_free').innerText = data.disk_free;
                document.getElementById('disk_usage').innerText = data.disk_usage;
                document.getElementById('cpu_temp').innerText = data.cpu_temp !== null ? data.cpu_temp : 'N/A';
                document.getElementById('private_ip').innerText = data.private_ip;
                document.getElementById('public_ip').innerText = data.public_ip;
                let gpuInfo = '';
                data.gpu_info.forEach(gpu => {
                    gpuInfo += `Name: ${gpu.gpu_name}, Load: ${gpu.gpu_load.toFixed(2)}%, Temp: ${gpu.gpu_temperature}°C<br>`;
                });
                document.getElementById('gpu_info').innerHTML = gpuInfo;
            } catch (error) {
                console.error('Error fetching system info:', error);
            }
        }

        setInterval(fetchSystemInfo, 5000);
        fetchSystemInfo();
    </script>
</head>
<body>
    <p>Press OK to continue to the page:</p>
    <button onclick="redirectToPage()">OK</button>
    <h3>Device Info</h3>
    <div class="info">
        <div>CPU Usage: <span id="cpu_usage"></span>%</div>
        <div>RAM Usage: <span id="ram_usage"></span>%</div>
        <div>Disk Total: <span id="disk_total"></span> GB</div>
        <div>Disk Used: <span id="disk_used"></span> GB</div>
        <div>Disk Free: <span id="disk_free"></span> GB</div>
        <div>Disk Usage: <span id="disk_usage"></span>%</div>
        <div>CPU Temperature: <span id="cpu_temp"></span>°C</div>
        <div>Private IP: <span id="private_ip"></span></div>
        <div>Public IP: <span id="public_ip"></span></div>
        <div>GPU Info: <span id="gpu_info"></span></div>
    </div>
</body>
</html>

📊 Example Output
When you open index.html in your browser, you will see the live system information updated every 5 seconds:
```
CPU Usage: 10%
RAM Usage: 40%
Disk Total: 256 GB
Disk Used: 128 GB
Disk Free: 128 GB
Disk Usage: 50%
CPU Temperature: 45°C
Private IP: 192.168.1.2
Public IP: 203.0.113.1
GPU Info: Name: NVIDIA GeForce GTX 1050, Load: 25%, Temp: 55°C
```

Feel free to contribute to this project by submitting issues or pull requests. Enjoy using Flask-ShadowStyle for your system monitoring needs!


### Notes

- Replace `https://github.com/yourusername/Flask-ShadowStyle.git` with the actual URL of your repository.
- Ensure that the `LICENSE` file is included in your repository if you mention it in the License section. If not, adjust the License section accordingly.
