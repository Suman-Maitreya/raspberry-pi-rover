// File: static/app.js
document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // --- CHART.JS SETUP ---
    const ctx = document.getElementById('sensorChart').getContext('2d');
    const sensorChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], datasets: [{
                label: 'Accel X (m/s)',
                data: [],
                borderColor: 'rgba(153, 102, 255, 1)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            scales: {
                y: { ticks: { color: '#e0e0e0' }, grid: { color: 'rgba(224, 224, 224, 0.2)' }},
                x: { ticks: { color: '#e0e0e0' }, grid: { color: 'rgba(224, 224, 224, 0.2)' }}
            },
            plugins: { legend: { labels: { color: '#e0e0e0' } } },
            responsive: true,
            maintainAspectRatio: false
        }
    });

    function addDataToChart(label, accelData) {
        sensorChart.data.labels.push(label);
        sensorChart.data.datasets[0].data.push(accelData);
        if (sensorChart.data.labels.length > 20) {
            sensorChart.data.labels.shift();
            sensorChart.data.datasets[0].data.shift();
        }
        sensorChart.update();
    }

    socket.on('connect', () => console.log('Connected to server!'));

    socket.on('update_sensors', function(data) {
        document.getElementById('temp-value').innerText = data.temp;
        document.getElementById('dist-value').innerText = data.distance;
        document.getElementById('accel-value').innerText = data.mpu.ax;

        const updateIrStatus = (elementId, isObstacle) => {
            const el = document.getElementById(elementId);
            el.innerText = isObstacle ? 'OBSTACLE' : 'CLEAR';
            el.className = isObstacle ? 'sensor-value obstacle' : 'sensor-value clear';
        };
        updateIrStatus('ir-status-1', data.ir_1);
        updateIrStatus('ir-status-2', data.ir_2);

        const time = new Date().toLocaleTimeString();
        addDataToChart(time, data.mpu.ax);
    });

    // --- CONTROL AND LOGGING BUTTONS ---
    const buttons = document.querySelectorAll('.control-btn');
    buttons.forEach(button => {
        const command = button.id.split('-')[1];
        const sendCommand = (cmd) => socket.emit('control_event', { data: cmd });
        button.addEventListener('mousedown', () => sendCommand(command));
        button.addEventListener('touchstart', (e) => { e.preventDefault(); sendCommand(command); });
        button.addEventListener('mouseup', () => sendCommand('stop'));
        button.addEventListener('touchend', (e) => { e.preventDefault(); sendCommand('stop'); });
    });
    
    const logButton = document.getElementById('btn-log');
    logButton.addEventListener('click', () => {
        socket.emit('toggle_logging');
    });

    socket.on('logging_status', function(data) {
        if (data.active) {
            logButton.textContent = 'STOP LOGGING';
            logButton.classList.add('active');
        } else {
            logButton.textContent = 'START LOGGING';
            logButton.classList.remove('active');
        }
    });

    // --- SPEED SLIDER ---
    const speedSlider = document.getElementById('speed-slider');
    const speedValue = document.getElementById('speed-value');
    speedSlider.addEventListener('input', () => speedValue.innerText = speedSlider.value);
    speedSlider.addEventListener('change', () => socket.emit('set_speed', { speed: speedSlider.value }));
});
