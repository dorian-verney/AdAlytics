// // wsListener.js
// let ws = null;

// // Callback function to handle received predictions
// let onPredictionCallback = null;

// export function initListener(socketUrl, callback) {
//     if (ws) return; // only one socket

//     onPredictionCallback = callback;

//     ws = new WebSocket(`${socketUrl}/api/ws`);

//     ws.onopen = () => {
//         console.log("Listener WebSocket connected");
//     };

//     ws.onmessage = (event) => {
//         console.log("RECEVIIIII", event.data);
//         const data = JSON.parse(event.data);
//         console.log("Received prediction:", data);

//         if (onPredictionCallback) {
//             onPredictionCallback(data); // let UI component handle it
//         }
//     };

//     ws.onclose = () => {
//         console.log("Listener WebSocket disconnected");
//         ws = null;
//     };

//     ws.onerror = (err) => {
//         console.error("Listener WebSocket error:", err);
//     };
// }
