<script>
    export let loading = false;
    
</script>

<button
    on:click
    class="px-6 py-3 bg-gray-800 text-white font-semibold 
           rounded-lg transition duration-200 ease-in-out flex items-center justify-center gap-2
           {loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-gray-900 hover:scale-105'}"
>
    {#if loading}
    <!-- Spinner -->
    <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"></path>
    </svg>
    {/if}
    <slot />
    
</button>



