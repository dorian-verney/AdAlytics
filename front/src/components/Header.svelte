<script>
  import { onMount } from "svelte";
  import { user } from "../stores/user";
  let notifications = 3;
  let firstLetterUsername = "?";
  let menuOpen = false;
  let menuEl;

  $: if ($user) {
    firstLetterUsername = $user.charAt(0).toUpperCase();
  }

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function closeMenu() {
    menuOpen = false;
  }

  function handleDeconnexion() {
    user.set(null);
    if (typeof localStorage !== "undefined") {
      localStorage.removeItem("user");
      localStorage.removeItem("loggedIn");
    }
    firstLetterUsername = "?";
    menuOpen = false;
    window.location.href = "/login";
  }

  function handleClickOutside(event) {
    if (menuEl && !menuEl.contains(event.target)) {
      closeMenu();
    }
  }

  onMount(() => {
    const stored = localStorage.getItem("user");
    if (stored && !$user) {
      user.set(stored);
    } else if (window.location.pathname === "/login") {
      user.set(null);
      localStorage.removeItem("user");
      localStorage.removeItem("loggedIn");
      firstLetterUsername = "?";
    }
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  });
</script>

<header class="bg-white shadow-md px-6 md:px-20 py-4 flex justify-between items-center">
  <!-- Logo -->
  <div class="flex items-center space-x-3">
    <div class="bg-purple-500 text-white font-bold rounded-full w-10 h-10 flex items-center justify-center">
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

    <div class="relative" bind:this={menuEl}>
      <button
        type="button"
        onclick={toggleMenu}
        class="w-10 h-10 rounded-full bg-gray-300 hover:bg-gray-400 transition cursor-pointer flex items-center justify-center text-gray-600 font-semibold focus:outline-none focus:ring-2 focus:ring-purple-500"
        aria-expanded={menuOpen}
        aria-haspopup="true"
      >
        {firstLetterUsername}
      </button>
      {#if menuOpen}
        <div
          class="absolute right-0 mt-2 w-56 rounded-lg bg-white shadow-lg ring-1 ring-black/5 py-1 z-50"
          role="menu"
        >
          <div class="px-4 py-2 text-gray-700 border-b border-gray-100">
            Welcome {$user ?? ""}
          </div>
          <button
            type="button"
            role="menuitem"
            onclick={handleDeconnexion}
            class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
          >
            Déconnexion
          </button>
        </div>
      {/if}
    </div>
  </div>
</header>
