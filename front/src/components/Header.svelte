<script>
  let notifications = 3;
</script>

<header class="bg-white shadow-md px-6 md:px-20 py-4 flex justify-between items-center">
  <!-- Logo -->
  <div class="flex items-center space-x-3">
    <div class="bg-blue-500 text-white font-bold rounded-full w-10 h-10 flex items-center justify-center">
      A
    </div>
    <span class="text-xl font-semibold text-gray-800">AdAlytics</span>
  </div>

  <!-- Navigation -->
  <nav class="hidden md:flex space-x-8 text-gray-600 font-medium">
    <a href="/" class="hover:text-gray-900 transition">Home</a>
    <a href="/" class="hover:text-gray-900 transition">About</a>
    <a href="/" class="hover:text-gray-900 transition">Services</a>
    <a href="/" class="hover:text-gray-900 transition">Contact</a>
  </nav>

  <!-- User / Notifications -->
  <div class="flex items-center space-x-4">
    <div class="relative cursor-pointer">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600 hover:text-gray-900 transition" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
      </svg>
      {#if notifications > 0}
        <span class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full text-xs w-5 h-5 flex items-center justify-center">{notifications}</span>
      {/if}
    </div>

    <div class="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center text-gray-600 font-semibold">
      DV
    </div>
  </div>
</header>
