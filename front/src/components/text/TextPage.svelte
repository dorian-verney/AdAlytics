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

<div class="w-full flex">
    <!-- Left side: Title + TextInput -->
    <div 
        class="overflow-hidden {isInspected ? 'w-1/2' : 'w-full'}"
        style="transition: width {duration_fade}ms ease-in-out;"
    >
        <h1 class="mb-20 text-3xl sm:text-5xl md:text-7xl font-bold">
            <span class="underline underline-offset-[24px]">Text </span> ad analysis.
        </h1>
        <div class="mt-4 px-8">
            <TextInput on:inspect-clicked={handleInspectClicked} />
        </div>
    </div>

    <!-- Right side: Chart (only visible after slide animation completes) -->
    {#if showChart}
        <div class="w-1/2">
            <AnalysisChart duration_fade={duration_fade} />
        </div>
    {/if}
</div>