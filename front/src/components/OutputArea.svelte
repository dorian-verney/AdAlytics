<script>
  import { fade } from 'svelte/transition';

  export let outputText = "";
  export let selectedTab = "metrics";
</script>

<div class="w-full bg-white rounded-md shadow p-6 min-h-[200px] relative overflow-hidden">
  {#if outputText}
    <p class="text-gray-800 whitespace-pre-wrap" transition:fade>{{outputText}}</p>
  {:else}
    <p class="text-gray-400 italic" transition:fade>
      {selectedTab === 'metrics' ? "Metrics will appear here..." : "Suggestions will appear here..."}
    </p>
  {/if}
</div>
