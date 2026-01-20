<script>
    export let selectedTab = "justification";
    export let onTabChange = () => {};
    export let mapping = [];

    function handleTabClick(tabId) {
        onTabChange(tabId);
    }

</script>

<div class="flex border-b border-gray-300 mb-3">
    {#each mapping as tab}
        <button
            onclick={() => handleTabClick(tab.id)}
            class="px-6 font-semibold text-lg text-gray-800 transition-colors duration-300 border-b-2 
                  {selectedTab === tab.id ? 'border-gray-800 text-black' : 'border-transparent hover:text-gray-800'}"
        >
            {tab.label}
        </button>
    {/each}
</div>
