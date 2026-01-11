// getWebSocketUrl.js
// Utility to determine the correct WebSocket URL based on environment

export function getWebSocketUrl() {
    if (typeof window === 'undefined') {
        // Server-side rendering fallback
        return 'ws://localhost:8000';
    }

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;

    console.log('host', host);
    console.log('protocol', protocol);

    // If running on localhost with a port (likely local dev), use port 8000 for backend
    if (host.includes('localhost') || host.includes('127.0.0.1')) {
        // Check if we're accessing through a specific port (like 4000 for frontend)
        // In local dev, backend is typically on 8000
        if (host.includes(':4321') || host.includes(':3000') || host.includes(':5173')) {
            return 'ws://localhost:8000';
        }
    }

    // For Docker/production, use the same host but with ws protocol
    return `${protocol}//${host}`;
}
