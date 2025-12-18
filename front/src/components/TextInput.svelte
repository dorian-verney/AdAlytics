<script>
    import Button from './Button.svelte';
    let loading = false;
    let inputText = "";
    let additionalText = "";

    async function handleClick() {
        loading = true;
        
        try {
            const response = await fetch('/api/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: inputText,
                    additional_context: additionalText
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
        } catch (error) {
            console.error('Error sending text to server:', error);
        } finally {
            loading = false;
        }
    }

</script>
<div>
    <div class="flex flex-col items-center w-full gap-4 mr-20">
        <h2 class="mb-2 sm:text-lg md:text-2xl text-gray-800 
                   ">
                   Enter your ad text and additional context below.
                   <span class="font-semibold">Inspect.</span>
        </h2>
        <textarea
            bind:value={inputText}
            placeholder="Write your ad text here..."
            class="w-1/2 px-6 py-5 rounded-lg border-2 border-gray-400 
                   bg-white shadow-lg focus:outline-none focus:ring-1 
                   focus:ring-gray-800 focus:border-gray-800 text-lg 
                   resize-y h-20 min-h-20"
        ></textarea>
        <textarea
            bind:value={additionalText}
            placeholder="Provide additional context..."
            class="w-1/2 px-4 py-4 rounded-md border border-gray-300 
                   focus:outline-none focus:ring-2 focus:ring-gray-800
                   focus:border-transparent text-sm resize-y h-16 min-h-16"
        ></textarea>
        <!-- Pass the loading prop to child -->
        <Button {loading} on:click={handleClick}>
            Inspect
        </Button>
    </div>
    
</div>
