<script>
    import Card from './Card.svelte';
    import background from '../../assets/background.svg';
    export let text = "Perfect for learning how the framework works, \
                       prototyping a new idea, or creating a demo to share online.";
</script>

<div>
    <h1 class="w-full mb-20 text-3xl sm:text-5xl md:text-7xl font-bold">
        <span class="underline underline-offset-[24px]">Welcome</span> to AdAlytics.
    </h1>
    <h2 class="w-full text-lg sm:text-xl md:text-2xl mb-10"> 
        Select your type of ads and get 
        <span class="font-bold">insights</span> on your ad 
        <span class="font-bold">performance</span>. 
    </h2>
    <div class="w-full flex flex-wrap justify-between gap-4">
        <Card type="Text" text={text} href="/text" />
        <Card type="Image" text={text} href="/" />
        <Card type="Video" text={text} href="/" />
    </div>
 
</div>
  

<!-- Upload your ads and get insights on your ad performance. -->