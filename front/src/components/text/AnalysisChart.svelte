<script>
    import { onMount, onDestroy } from 'svelte';
    import { fade } from 'svelte/transition';
    import { initWebSocket, subscribe, getWebSocketUrl } from "../../utils/websockets.js";
    let unsubscribe = null;

    import ScoreTab from '../ScoreTab.svelte';
    import SlideBar from '../SlideBar.svelte';
    import OutputText from './OutputText.svelte';
    import ProgressBar from '../ProgressBar.svelte';

    export let selectedTab = "justification";
    let scores = [];
    let justification = "";
    let suggestions = "";
    let new_ad = "";
    let progress = 0;
    let showProgressBar = false;
    let showResults = false;  // Only show results when critic stage is reached
    export let duration_fade;

    const tabs = [
        { id: "justification", label: "Justification" },
        { id: "suggestions", label: "Suggestions" }, 
        { id: "new_ad", label: "New Ad Example" }
    ];

    function handleTabChange(tab) {
        selectedTab = tab;
    }

    function updateScores(result) {
        scores = Object.entries(result)
                    .filter(([key]) => key !== 'justification')
                    .map(([key, value]) => {
                        // Handle both string and numeric values
                        const scoreValue = typeof value === 'string' ? parseInt(value) : value;
                        return {
                            label: key.split('_').map(word => 
                                word.charAt(0).toUpperCase() + word.slice(1)
                            ).join(' '),
                            score: scoreValue / 10  // Convert 0-10 scale to 0-1 scale
                        };
                    });
    }

    // Track current stage to detect new requests (scorer or critic)
    let currentStage = null;

    // Process complete results from the backend
    function processStreamData(data) {
        // Reset state when a new request starts (new scorer stage)
        if (data.stage === "scorer" && currentStage !== "scorer") {
            scores = [];
            justification = "";
            suggestions = "";
            new_ad = "";
            progress = 0;
            showProgressBar = true;
            showResults = false;  // Hide results until critic stage
        }
        
        // When critic stage is reached, show scores and justification
        if (data.stage === "critic" && currentStage !== "critic") {
            showResults = true;
        }
        
        currentStage = data.stage;

        // Update progress
        if (data.progress !== undefined) {
            progress = data.progress;
            showProgressBar = progress < 100;
        }

        // Process scorer stage results (store directly, display when critic stage is reached)
        if (data.stage === "scorer" && data.result) {
            const result = data.result;
            
            // Update scores
            if (result.clarity !== undefined || result.brand_alignment !== undefined) {
                updateScores(result);
            }
            
            // Update justification
            if (result.justification) {
                justification = result.justification;
            }
        }

        // Process critic stage results (suggestions + new_ad)
        if (data.stage === "critic" && data.result) {
            const result = data.result;
            
            // Update suggestions (array to string)
            if (result.suggestions && Array.isArray(result.suggestions)) {
                suggestions = result.suggestions.join('\n\n');
            } else if (result.suggestions) {
                suggestions = result.suggestions;
            }
            
            // Update new_ad
            if (result.new_ad) {
                new_ad = result.new_ad;
            }
        }
    }


    onMount(() => {
        const wsUrl = getWebSocketUrl();
        // Initialize WebSocket if not already initialized
        initWebSocket(wsUrl);
        // Subscribe to messages
        unsubscribe = subscribe((data) => {
            console.log("Received prediction from backend: ", data);
            processStreamData(data);
        });
    });

    onDestroy(() => {
        // Clean up subscription when component unmounts
        if (unsubscribe) {
            unsubscribe();
        }
    });


</script>


<div class="w-full px-8 flex-shrink-0" transition:fade={{ duration: duration_fade/2 }}>
    <div class="h-full bg-white rounded-lg border-2 border-gray-300 shadow-lg p-6 flex flex-col">
        <h2 class="text-2xl font-bold mb-6 text-gray-800">Analysis Chart</h2>
        
        <!-- Progress Bar -->
        <ProgressBar progress={progress} show={showProgressBar} message="Processing analysis..." />
        
        <!-- Vertical Bar Chart - Always displayed -->
        <ScoreTab {scores} />
        
        <!-- Results Area at Bottom - Always displayed -->
        <div class="mt-auto border-t-2 border-gray-200 pt-4 min-h-0 flex-shrink">
            <h3 class="text-xl font-semibold text-gray-700 mb-3">Analysis Results</h3>
            <SlideBar mapping={tabs} selectedTab={selectedTab} onTabChange={handleTabChange} />
            <div class="min-h-0">
                {#if selectedTab === tabs[0].id}
                    <OutputText typeOfText={tabs[0].label} dataText={justification} />
                {:else if selectedTab === tabs[1].id}
                    <OutputText typeOfText={tabs[1].label} dataText={suggestions} />
                {:else if selectedTab === tabs[2].id}
                    <OutputText typeOfText={tabs[2].label} dataText={new_ad} />
                {/if}
            </div>
        </div>

    </div>
</div>