const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let lastX = 0;
let lastY = 0;

ctx.strokeStyle = 'white';
ctx.lineWidth = 10;
ctx.lineCap = 'round';
ctx.lineJoin = 'round';

canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    [lastX, lastY] = [e.offsetX, e.offsetY];
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.closePath();
});

canvas.addEventListener('mouseout', () => {
    drawing = false;
    ctx.closePath();
});

canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    const currentX = e.offsetX;
    const currentY = e.offsetY;
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(currentX, currentY);
    ctx.stroke();
    [lastX, lastY] = [currentX, currentY];
});

document.getElementById('clearBtn').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    document.getElementById('result').textContent = '';
});

document.getElementById('predictBtn').addEventListener('click', () => {
    const imageData = canvas.toDataURL('image/png');
    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: imageData })
    })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById('result');
            if (data.error) {
                resultDiv.textContent = 'Ошибка: ' + data.error;
                resultDiv.style.color = 'red';
            } else {
                resultDiv.textContent = `Распознанная цифра: ${data.digit}`;
                resultDiv.style.color = "var(--accent-color)";
            }
        });
});
