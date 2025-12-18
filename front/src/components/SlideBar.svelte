<script>
    export let selectedTab = "text";
    export let onTabChange = () => {};
    
    const tabs = [
        { id: "text", label: "Text" },
        { id: "score", label: "Score" },
        { id: "suggestions", label: "Suggestions" }
    ];

    function handleTabClick(tabId) {
        onTabChange(tabId);
    }

</script>

<div class="flex border-b border-gray-300 mb-6">
    {#each tabs as tab}
        <button
            onclick={() => handleTabClick(tab.id)}
            class="px-6 py-3 font-semibold text-gray-800 transition-colors duration-300 border-b-2 
                  {selectedTab === tab.id ? 'border-gray-800 text-black' : 'border-transparent hover:text-gray-800'}"
        >
            {tab.label}
        </button>
    {/each}
</div>
