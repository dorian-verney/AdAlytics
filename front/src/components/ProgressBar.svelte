<script>
    export let progress = 0; // 0-100
    export let message = "Processing...";
    export let show = false;
</script>

{#if show}
    <div class="w-full mb-4">
        <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">{message}</span>
            <span class="text-sm font-medium text-gray-700">{Math.round(progress)}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div 
                class="bg-purple-500 h-2.5 rounded-full transition-all duration-300 ease-out"
                style="width: {progress}%"
            ></div>
        </div>
    </div>
{/if}
