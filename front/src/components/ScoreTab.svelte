<script>
    export let scores = [];
   
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

<div class="space-y-6">
    {#each scores as res}
        <div>
            <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold text-gray-800">
                    {res.label || 'Score'}
                </h3>
                <span class="text-lg font-bold text-indigo-600">
                    {Math.round((res.score || 0) * 100)}%
                </span>
            </div>
            <div class="w-full bg-gray-100 rounded-full h-4">
                <div
                    class="bg-linear-to-r from-violet-400 to-violet-200 h-4 rounded-full transition-all duration-300"
                    style="width: {(res.score || 0) * 100}%"
                ></div>
            </div>
        </div>
    {/each}
    
    {#if scores.length === 0}
        <p class="text-gray-500 text-center py-8">No prediction results yet. Submit text to see scores.</p>
    {/if}
</div>

