<script>
    export let suggestions = "";
    export let onSuggestionsChange = (value) => {};
</script>

<textarea
    value={suggestions}
    oninput={(e) => {
        suggestions = e.target.value;
        onSuggestionsChange(suggestions);
    }}
    placeholder="Suggestions will appear here..."
    class="w-full min-h-[400px] px-4 py-4 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent text-lg resize-none"
></textarea>

