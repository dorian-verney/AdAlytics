<script>
    import { onMount, onDestroy } from 'svelte';
    
    export let text = "";
    export let onTextChange = (value) => {};
    
    
    
</script>

<textarea
    value={text}
    oninput={(e) => {
        text = e.target.value;
        onTextChange(text);
    }}
    placeholder="Summary will appear here..."
    class="w-full min-h-[200px] px-4 py-4 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:border-transparent text-lg resize-none"
></textarea>

