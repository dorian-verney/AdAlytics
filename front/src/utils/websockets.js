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
            lastMessage = null;
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

// FOR TOKEN STREAMING
// /**
//  * Send a text generation request with streaming tokens
//  * @param {string} prompt - The prompt text
//  * @param {number} maxNewTokens - Maximum number of tokens to generate (default: 50)
//  * @param {Function} onToken - Callback called for each token received
//  * @param {Function} onStart - Callback called when streaming starts
//  * @param {Function} onEnd - Callback called when streaming ends
//  */
// export function sendTextGenerationStream(prompt, maxNewTokens = 50, onToken = null, onStart = null, onEnd = null) {
//     if (!ws || ws.readyState !== WebSocket.OPEN) {
//         console.error("Can't Send Text: WebSocket not connected");
//         return;
//     }
    
//     // Set up a temporary callback to handle streaming messages
//     const streamCallback = (data) => {
//         if (data.type === "stream_start") {
//             if (onStart) onStart(data);
//         } else if (data.type === "token") {
//             if (onToken) onToken(data.token);
//         } else if (data.type === "stream_end") {
//             if (onEnd) onEnd(data);
//             // Unsubscribe after streaming ends
//             unsubscribe(streamCallback);
//         }
//     };
    
//     // Subscribe to handle streaming messages
//     subscribe(streamCallback, false);
    
//     // Send the streaming request
//     ws.send(JSON.stringify({
//         text: prompt,
//         type: "text-generation",
//         stream: true,
//         max_new_tokens: maxNewTokens
//     }));
// }

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
    const port = window.location.port;

    // If running on localhost
    if (host.includes('localhost') || host.includes('127.0.0.1')) {
        // If accessing through port 80 (Traefik/Docker), use same host
        if (port === '80' || port === '' || !port) {
            return `${protocol}//${host.split(':')[0]}`;
        }
        // For local dev (frontend on dev port), try direct backend connection on 8000
        // This assumes backend is running locally or Docker port 8000 is exposed
        return 'ws://localhost:8000';
    }
    // For Docker/production, use the same host but with ws protocol
    return `${protocol}//${host}`;
}