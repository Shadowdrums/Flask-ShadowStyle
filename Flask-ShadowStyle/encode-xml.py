import base64

html_content = """<!DOCTYPE html>
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

        // Fetch system info every 5 seconds
        setInterval(fetchSystemInfo, 5000);
        fetchSystemInfo(); // initial fetch
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
"""
#Encode the HTML content to hex
html_hex = html_content.encode('utf-8').hex()

# Encode the hex to base64
html_base64 = base64.b64encode(bytes.fromhex(html_hex)).decode('utf-8')

# Display the base64 encoded string
print(html_base64)
