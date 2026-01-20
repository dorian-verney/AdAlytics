<script>
    let TmpScores = [
        // {label: "Sentiment", score: 85},
        // {label: "Engagement", score: 75},
        // {label: "Explainability", score: 65},
    ];

    export let scores = []
    function processPredScores(data) {
        // Get the array of results (result[0] contains the array)
        let results = Array.isArray(data[0]) 
            ? data[0] 
            : data;
        
        // Sort by score in descending order (highest first)
        scores = results.sort((a, b) => (b.score || 0) - (a.score || 0));
    }

    $: processPredScores(scores);
       

</script>

<div class="flex-1 flex items-end justify-center gap-8 mb-8">
    {#if scores.length > 0}
        {#each scores as metric}
        <div class="flex flex-col items-center gap-2">
            <span class="text-sm font-bold text-gray-900">{Math.round(metric.score*100)}%</span>
            <div class="w-16 bg-gray-200 rounded-t-lg h-64 flex flex-col justify-end">
                <div 
                    class="bg-purple-500 rounded-t-lg transition-all duration-500 ease-out"
                    style="height: {metric.score*100}%"
                ></div>
            </div>
            <span class="text-sm font-semibold text-gray-700">{metric.label}</span>
        </div>
        {/each}
    {:else}
        <div class="flex flex-col items-center gap-2">
            <span class="text-lg font-semibold text-gray-700">No scores available yet...</span>
        </div>
    {/if}
</div>

