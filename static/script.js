function startDetection() {
    fetch('/start_detection')
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            updateUI(true);
            showNotification('Detection Started', 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error starting detection', 'error');
        });
}

function stopDetection() {
    fetch('/stop_detection')
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            updateUI(false);
            showNotification('Detection Stopped', 'info');
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error stopping detection', 'error');
        });
}

function closeCamera() {
    fetch('/close_camera')
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
            updateUI(false);
            document.getElementById('detection-status').textContent = 'Camera closed';
            showNotification('Camera Closed', 'info');
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error closing camera', 'error');
        });
}

function updateUI(isDetecting) {
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const statusText = document.getElementById('status-text');
    const detectionStatus = document.getElementById('detection-status');

    if (isDetecting) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusText.textContent = 'Detecting';
        detectionStatus.textContent = '🔴 Live Detection Active';
        document.querySelector('.status-indicator').style.background = 'rgba(76, 175, 80, 0.9)';
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusText.textContent = 'Ready';
        detectionStatus.textContent = '⚫ Detection Paused';
        document.querySelector('.status-indicator').style.background = 'rgba(0, 0, 0, 0.7)';
    }
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        animation: slideIn 0.3s ease-out;
        z-index: 1000;
    `;

    if (type === 'success') {
        notification.style.background = '#4CAF50';
    } else if (type === 'error') {
        notification.style.background = '#f44336';
    } else {
        notification.style.background = '#2196F3';
    }

    notification.textContent = message;
    document.body.appendChild(notification);

    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize UI on page load
window.addEventListener('load', () => {
    updateUI(false);
});
