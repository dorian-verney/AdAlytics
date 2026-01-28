<script>
    import Button from '../Button.svelte';
    import { onMount, createEventDispatcher } from 'svelte';
    let loading = false;
    let inputText = "";
    let additionalText = "";
    import { initWebSocket, sendText, getWebSocketUrl } from "../../utils/websockets.js";
    
    const dispatch = createEventDispatcher();
    
    onMount(() => {
        const wsUrl = getWebSocketUrl();
        console.log("TextInput mounted - WS URL: ", wsUrl);
        // Initialize WebSocket connection (no callback needed - this component only sends)
        initWebSocket(wsUrl);
    });

    // On button click
    function handleClickWs() {
        console.log("Sending text to server", inputText);
        sendText(inputText, additionalText);
        // Emit event to parent to trigger slide animation
        dispatch('inspect-clicked');
    }

</script>
<div>
    <div class="flex flex-col items-center w-full gap-4 mr-20">
        <h2 class="mb-2 sm:text-lg md:text-2xl text-gray-800 
                   ">
                   Enter your ad text and additional context below.
                   <span class="font-semibold">Inspect.</span>
        </h2>
        <textarea
            bind:value={inputText}
            placeholder="Write your ad text here..."
            class="w-1/2 min-w-3/4 px-6 py-5 rounded-lg border-2 border-gray-400 
                   bg-white shadow-lg focus:outline-none focus:ring-1 
                   focus:ring-gray-800 focus:border-gray-800 text-lg 
                   resize-y h-20 min-h-20 "
        ></textarea>
        <textarea
            bind:value={additionalText}
            placeholder="Provide additional context..."
            class="w-1/2 min-w-3/4 px-4 py-4 rounded-md border border-gray-300 
                   focus:outline-none focus:ring-2 focus:ring-gray-800
                   focus:border-transparent text-sm resize-y h-16 min-h-16"
        ></textarea>
        <!-- Pass the loading prop to child -->
        <Button {loading} on:click={handleClickWs}>
            Inspect
        </Button>
    </div>
    
</div>
