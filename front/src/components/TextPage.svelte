<script>
    import TextInput from './TextInput.svelte';
    import SlideBar from './SlideBar.svelte';
    import TextTab from './TextTab.svelte';
    import ScoreTab from './ScoreTab.svelte';
    import SuggestionsTab from './SuggestionsTab.svelte';
    
    let selectedTab = "text";
    let tabText = "";
    let engagementScore = 75;
    let sentimentScore = 82;
    let explainabilityScore = 68;
    let suggestions = "";
    
    function handleTabChange(tab) {
        selectedTab = tab;
    }
    
    function handleTextChange(value) {
        tabText = value;
    }
    
    function handleSuggestionsChange(value) {
        suggestions = value;
    }
    
</script>

<div>
    <h1 class="w-full mb-10 text-xl sm:text-2xl md:text-5xl font-bold">
        <span class="underline underline-offset-12px">Text ad</span> analysis.
    </h1>
    <TextInput />
    
    <div class="pl-6">
        <SlideBar {selectedTab} onTabChange={handleTabChange} />
        {#if selectedTab === "text"}
            <TextTab text={tabText} onTextChange={handleTextChange} />
        {:else if selectedTab === "score"}
            <ScoreTab {engagementScore} {sentimentScore} {explainabilityScore} />
        {:else if selectedTab === "suggestions"}
            <SuggestionsTab {suggestions} onSuggestionsChange={handleSuggestionsChange} />
        {/if}
    </div>
</div>