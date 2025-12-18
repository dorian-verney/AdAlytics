<script>
    import { onMount, onDestroy } from 'svelte';

    let eventSource = null;
    let reconnectTimeout = null;
    let predictionResults = [];
        
    function connectSSE() {
        if (eventSource) {
            eventSource.close();
        }
        
        eventSource = new EventSource('/api/stream');
        
        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log(data);
                if (data.prediction && data.prediction.result) {
                    // Get the array of results (result[0] contains the array)
                    let results = Array.isArray(data.prediction.result[0]) 
                        ? data.prediction.result[0] 
                        : data.prediction.result;
                    
                    // Sort by score in descending order (highest first)
                    predictionResults = results.sort((a, b) => (b.score || 0) - (a.score || 0));
                }
            } catch (error) {
                console.error('Error parsing SSE data:', error);
            }
        };
        
        eventSource.onerror = (error) => {
            if (eventSource.readyState === EventSource.CLOSED) {
                console.log('SSE connection closed, reconnecting...');
                // Reconnect after a short delay
                reconnectTimeout = setTimeout(() => {
                    connectSSE();
                }, 3000);
            }
        };
    }
    
    onMount(() => {
        connectSSE();
        
        return () => {
            if (reconnectTimeout) {
                clearTimeout(reconnectTimeout);
            }
            if (eventSource) {
                eventSource.close();
            }
        };
    });
    
    onDestroy(() => {
        if (reconnectTimeout) {
            clearTimeout(reconnectTimeout);
        }
        if (eventSource) {
            eventSource.close();
        }
    });
</script>

<div class="space-y-6">
    {#each predictionResults as result}
        <div>
            <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold text-gray-800">
                    {result.label || 'Score'}
                </h3>
                <span class="text-lg font-bold text-indigo-600">
                    {Math.round((result.score || 0) * 100)}%
                </span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-4">
                <div
                    class="bg-linear-to-r from-violet-400 to-violet-200 h-4 rounded-full transition-all duration-300"
                    style="width: {(result.score || 0) * 100}%"
                ></div>
            </div>
        </div>
    {/each}
    
    {#if predictionResults.length === 0}
        <p class="text-gray-500 text-center py-8">No prediction results yet. Submit text to see scores.</p>
    {/if}
</div>

