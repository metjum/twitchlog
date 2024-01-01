document.addEventListener('DOMContentLoaded', function() {
    // Získání aktuálního data
    const currentDate = new Date();
    const year = currentDate.getFullYear();
    const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
    const day = currentDate.getDate().toString().padStart(2, '0');

    // Sestavení názvu souboru s aktuálním datem
    const logFileName = `agraelus-${year}-${month}-${day}.log`;

    // Vytvoření XMLHttpRequest s aktuálním názvem souboru
    const xhr = new XMLHttpRequest();
    xhr.open('GET', logFileName, true);

    // Ostatní části kódu zůstávají nezměněné

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            const logContent = xhr.responseText;
            const logLines = logContent.split('\n');
            const logContainer = document.getElementById('logContainer');
            logLines.forEach(function(line) {
                if (!line.trim().startsWith('//')) {
                    const logMessage = document.createElement('div');
                    logMessage.className = 'logMessage';
                    logMessage.textContent = line;
                    const randomColor = getRandomColor();
                    logMessage.style.color = randomColor;
                    logContainer.appendChild(logMessage);
                }
            });
        }
    };

    xhr.send();

    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();
        const logMessages = document.querySelectorAll('.logMessage');
        logMessages.forEach(function(logMessage) {
            const messageText = logMessage.textContent.toLowerCase();
            if (messageText.includes(searchTerm)) {
                logMessage.style.display = 'block';
            } else {
                logMessage.style.display = 'none';
            }
        });
    });

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
});
