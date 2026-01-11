export let ws = null;
// Array to store multiple callbacks for different components
let messageCallbacks = new Set();
// Cache the last received message so late subscribers can get it immediately
let lastMessage = null;

export function initWebSocket(socketUrl, callback = null) {
    if (!ws) {
        console.log("Creating NEW WebSocket connection");
        ws = new WebSocket(`${socketUrl}/api/ws`);
        
        ws.onopen = () => {
            console.log("WebSocket connected");
        };
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                // Store the last message for late subscribers
                lastMessage = data;
                // Call all registered callbacks
                messageCallbacks.forEach(callback => {
                    try {
                        callback(data);
                    } catch (error) {
                        console.error("Error in WebSocket callback:", error);
                    }
                });
            } catch (error) {
                console.error("Error parsing WebSocket message:", error);
            }
        };

        ws.onclose = () => {
            console.log("WebSocket disconnected");
            ws = null; // allow reconnect
            messageCallbacks.clear(); // Clear callbacks on disconnect
            lastMessage = null; // Clear cached message on disconnect
        };
        
        ws.onerror = (err) => {
            console.error("WebSocket error:", err);
        };
    } else {
        console.log("WebSocket already exists, reusing existing connection");
    }
    
    // If a callback is provided, subscribe it
    if (callback) {
        subscribe(callback);
    }
}

/**
 * Subscribe to WebSocket messages
 * @param {Function} callback - Function to call when a message is received
 * @param {boolean} receiveLastMessage - If true, immediately call callback with last message if available
 * @returns {Function} Unsubscribe function
 */
export function subscribe(callback, receiveLastMessage = true) {
    if (typeof callback !== 'function') {
        console.warn("subscribe: callback must be a function");
        return () => {};
    }
    
    messageCallbacks.add(callback);
    console.log(`Subscribed callback. Total subscribers: ${messageCallbacks.size}`);
    
    // If there's a cached last message, immediately call the callback with it
    if (receiveLastMessage && lastMessage !== null) {
        try {
            console.log("Calling new subscriber with last cached message");
            callback(lastMessage);
        } catch (error) {
            console.error("Error calling callback with last message:", error);
        }
    }
    
    // Return unsubscribe function
    return () => unsubscribe(callback);
}

/**
 * Get the last received message without subscribing
 * @returns {Object|null} The last message received, or null if none
 */
export function getLastMessage() {
    return lastMessage;
}

/**
 * Unsubscribe from WebSocket messages
 * @param {Function} callback - The callback function to remove
 */
export function unsubscribe(callback) {
    messageCallbacks.delete(callback);
    console.log(`Unsubscribed callback. Total subscribers: ${messageCallbacks.size}`);
}

// Legacy function - kept for backward compatibility but not recommended
export function getWebSocketMessageCallback(callback = null) {
    if (callback) {
        subscribe(callback);
    }
}


// Send text to backend for prediction
// TODO: sometimes, it is not inputText, additionalContext
// insert in args a custom class corresponding to type of data to send
export function sendText(inputText, additionalContext = "") {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        console.error("Can't Send Text: WebSocket not connected");
        return;
    }
    ws.send(JSON.stringify({
        text: inputText,
        additional_context: additionalContext
    }));
}

// --------------------------------------------------------------
// Utility to determine the correct WebSocket URL based on environment
// --------------------------------------------------------------
export function getWebSocketUrl() {
    if (typeof window === 'undefined') {
        // Server-side rendering fallback
        return 'ws://localhost:8000';
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;

    // If running on localhost with a port (likely local dev), use port 8000 for backend
    if (host.includes('localhost') || host.includes('127.0.0.1')) {
        // Check if we're accessing through a specific port (like 4321 for frontend)
        // In local dev, backend is typically on 8000
        if (host.includes(':4321') || host.includes(':3000') || host.includes(':5173')) {
            return 'ws://localhost:8000';
        }
    }
    // For Docker/production, use the same host but with ws protocol
    return `${protocol}//${host}`;
}