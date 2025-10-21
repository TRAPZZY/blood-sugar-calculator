// Main JavaScript file

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
});

// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Form validation
function validateReadingForm(form) {
    const value = parseFloat(form.value.value);

    if (isNaN(value) || value <= 0 || value > 600) {
        alert('Please enter a valid blood sugar value between 0 and 600 mg/dL');
        return false;
    }

    return true;
}

function validateGoalForm(form) {
    const min = parseFloat(form.target_min.value);
    const max = parseFloat(form.target_max.value);

    if (isNaN(min) || isNaN(max)) {
        alert('Please enter valid numbers for target range');
        return false;
    }

    if (min >= max) {
        alert('Target minimum must be less than target maximum');
        return false;
    }

    if (min < 0 || max > 600) {
        alert('Target values must be between 0 and 600 mg/dL');
        return false;
    }

    return true;
}

// Set current date/time as default for reading form
function setCurrentDateTime() {
    const input = document.getElementById('reading_time');
    if (input) {
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');

        input.value = `${year}-${month}-${day}T${hours}:${minutes}`;
    }
}

// Initialize datetime input on page load
document.addEventListener('DOMContentLoaded', setCurrentDateTime);

// Blood sugar status indicator
function getBloodSugarStatus(value) {
    if (value < 70) {
        return { class: 'status-critical-low', text: 'Critical Low', badge: 'badge-danger' };
    } else if (value < 100) {
        return { class: 'status-low', text: 'Low', badge: 'badge-warning' };
    } else if (value <= 130) {
        return { class: 'status-normal', text: 'Normal', badge: 'badge-success' };
    } else if (value <= 150) {
        return { class: 'status-elevated', text: 'Elevated', badge: 'badge-warning' };
    } else {
        return { class: 'status-high', text: 'High', badge: 'badge-danger' };
    }
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Create chart for blood sugar readings
function createBloodSugarChart(canvasId, labels, data, goals = []) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const chartData = {
        labels: labels,
        datasets: [{
            label: 'Blood Sugar (mg/dL)',
            data: data,
            borderColor: 'rgb(37, 99, 235)',
            backgroundColor: 'rgba(37, 99, 235, 0.1)',
            tension: 0.4,
            fill: true
        }]
    };

    // Add goal ranges as background areas
    const annotations = {};
    goals.forEach((goal, index) => {
        annotations[`goal${index}`] = {
            type: 'box',
            yMin: goal.target_min,
            yMax: goal.target_max,
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            borderColor: 'rgba(16, 185, 129, 0.5)',
            borderWidth: 1
        };
    });

    new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Blood Sugar Trends'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Blood Sugar (mg/dL)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                }
            }
        }
    });
}

// Create distribution chart
function createDistributionChart(canvasId, distribution) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical Low (<70)', 'Low (70-99)', 'Normal (100-130)', 'Elevated (131-150)', 'High (>150)'],
            datasets: [{
                data: [
                    distribution.critical_low,
                    distribution.low,
                    distribution.normal,
                    distribution.elevated,
                    distribution.high
                ],
                backgroundColor: [
                    'rgb(239, 68, 68)',
                    'rgb(245, 158, 11)',
                    'rgb(16, 185, 129)',
                    'rgb(245, 158, 11)',
                    'rgb(239, 68, 68)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'Blood Sugar Distribution'
                }
            }
        }
    });
}

// Load chart data from API
async function loadChartData(endpoint, canvasId, chartType) {
    try {
        const response = await fetch(endpoint);
        const data = await response.json();

        if (chartType === 'line') {
            createBloodSugarChart(canvasId, data.labels, data.values);
        } else if (chartType === 'distribution') {
            createDistributionChart(canvasId, data);
        }
    } catch (error) {
        console.error('Error loading chart data:', error);
    }
}

// Export table to CSV
function exportTableToCSV(tableId, filename) {
    const table = document.getElementById(tableId);
    if (!table) return;

    let csv = [];
    const rows = table.querySelectorAll('tr');

    for (let row of rows) {
        let rowData = [];
        const cols = row.querySelectorAll('td, th');

        for (let col of cols) {
            rowData.push('"' + col.innerText.replace(/"/g, '""') + '"');
        }

        csv.push(rowData.join(','));
    }

    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'export.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}
