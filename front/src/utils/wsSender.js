// wsSender.js
let ws = null;
let onMessageCallback = null;

export function initWebSocket(socketUrl, callback = null) {
    if (!ws) {
        onMessageCallback = callback;
        ws = new WebSocket(`${socketUrl}/api/ws`);

        ws.onopen = () => {
            console.log("WebSocket connected");
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);                
                if (onMessageCallback) {
                    onMessageCallback(data);
                }
            } catch (error) {
                console.error("Error parsing WebSocket message:", error);
            }
        };

        ws.onclose = () => {
            console.log("WebSocket disconnected");
            ws = null; // allow reconnect
        };

        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        };
    } else if (callback) {
        // Update callback if WebSocket already exists
        onMessageCallback = callback;
    }
}

// Send text to backend for prediction
export function sendText(inputText, additionalContext = "") {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        console.error("WebSocket not connected");
        return;
    }

    console.log("WS is OKAY")

    ws.send(JSON.stringify({
        text: inputText,
        additional_context: additionalContext
    }));
}
