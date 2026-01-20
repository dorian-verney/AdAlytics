<script>
    import TextInput from './TextInput.svelte';
    import AnalysisChart from './AnalysisChart.svelte';
    let duration_fade = 1000;
    let isInspected = false; // Track if inspect button was clicked
    let showChart = false; // Track when to show chart (after slide animation completes)

    function handleInspectClicked() {
        isInspected = true;
        // Show chart after 1000ms (when slide animation completes)
        setTimeout(() => {
            showChart = true;
        }, duration_fade+0.2*duration_fade);
    }
    
</script>

<div class="w-full">
    <h1 class="w-full mb-10 text-xl sm:text-2xl md:text-5xl font-bold">
        <span class="underline underline-offset-12px">Text ad</span> analysis.
    </h1>
    
    <div class="flex w-full gap-4">
        <!-- Left side: TextInput -->
        <div 
            class="mt-24 overflow-hidden px-8 {isInspected ? 'w-1/2' : 'w-full'}"
            style="transition: width {duration_fade}ms ease-in-out;"
        >
            <TextInput on:inspect-clicked={handleInspectClicked} />
        </div>
        
        <!-- Right side: Chart (only visible after slide animation completes) -->
        {#if showChart}
            <AnalysisChart duration_fade={duration_fade} />
        {/if}
    </div>
    
 
</div>