<script>
    import TextInput from './TextInput.svelte';
    import SlideBar from './SlideBar.svelte';
    import TextTab from './TextTab.svelte';
    import ScoreTab from './ScoreTab.svelte';
    import SuggestionsTab from './SuggestionsTab.svelte';
    import { onMount, onDestroy } from 'svelte';
    import { initWebSocket, subscribe, getWebSocketUrl } from "../utils/websockets.js";
    let unsubscribe = null;
    
    let selectedTab = "text";
    let textSummary = "";
    let scores = [];
    let engagementScore = 75;
    let sentimentScore = 82;
    let explainabilityScore = 68;
    let suggestions = "";

    function handleTabChange(tab) {
        selectedTab = tab;
    }
    
    onMount(() => {
        const wsUrl = getWebSocketUrl();
        // Initialize WebSocket if not already initialized
        initWebSocket(wsUrl);
        // Subscribe to messages
        unsubscribe = subscribe((predictionData) => {
            console.log("Received prediction from TextTab: ", predictionData);
            assignPredData(predictionData);
        });
    });

    onDestroy(() => {
        // Clean up subscription when component unmounts
        if (unsubscribe) {
            unsubscribe();
        }
    });


    function assignPredData(predictionData) {
        if (predictionData.prediction) {
            let pred = predictionData.prediction;
            if (pred.text) {
                textSummary = pred.text;
            }
            if (pred.scores) {
                scores = pred.scores;
            }
            if (pred.suggestions) {
                suggestions = pred.suggestions;
            }
        }
    }
    
</script>

<div>
    <h1 class="w-full mb-10 text-xl sm:text-2xl md:text-5xl font-bold">
        <span class="underline underline-offset-12px">Text ad</span> analysis.
    </h1>
    <TextInput />
    
    <div class="pl-6">
        <SlideBar {selectedTab} onTabChange={handleTabChange} />
        {#if selectedTab === "text"}
            <TextTab text={textSummary} />
        {:else if selectedTab === "score"}
            <ScoreTab {scores} />
        {:else if selectedTab === "suggestions"}
            <SuggestionsTab {suggestions} />
        {/if}
    </div>
</div>