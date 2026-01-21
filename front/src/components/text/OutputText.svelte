<script>
    export let typeOfText = "";
    export let dataText = "";  
    let textarea;
    
    // Auto-resize textarea to fit content
    function autoResize() {
        if (textarea) {
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
            // Scroll to top when content changes
            textarea.scrollTop = 0;
        }
    }
    
    // Handle both string and array for backward compatibility
    $: formattedText = typeof dataText === 'string' ? dataText : (Array.isArray(dataText) ? dataText.join('\n') : '');
    
    $: if (formattedText && textarea) {
        autoResize();
    }
</script>

<div class="select-none">
    <textarea
        bind:this={textarea}
        value={formattedText}
        readonly
        placeholder={typeOfText + " will appear here..."}
        class="w-full px-4 min-h-[150px] max-h-[600px] py-4 rounded-md border border-gray-200 focus:outline-none focus:ring-0 focus:border-gray-200 text-lg resize-y overflow-y-auto cursor-default"
        on:input={autoResize}
    ></textarea>
</div>

