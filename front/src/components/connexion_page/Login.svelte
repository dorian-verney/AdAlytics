<script>
    export let username = "";
    export let password = "";
    export let status = "idle";
    export let handleLogin = async () => {};
    let errorMessagePassword;

    $: if (status === "idle") {
        errorMessagePassword = "Please choose a password.";
    } else if (status === "error") {
        errorMessagePassword = "Wrong password. Please try again.";
    } else if (status === "success") {
        errorMessagePassword = "";
    }

</script>

<div class="w-full max-w-md">
    <form class="bg-white shadow-md rounded-xl px-8 pt-6 pb-8 mb-4">
      <div class="mb-4">
        <label class="block text-gray-700 text-lg font-bold mb-2" for="username">
          Username
        </label>
        <input bind:value={username} class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" placeholder="Username">
      </div>
      <div class="mb-6">
        <label class="block text-gray-700 text-lg font-bold mb-2" for="password">
          Password
        </label>
        <input bind:value={password} class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" placeholder="******************">
        <p class="text-red-500 text-xs italic">{errorMessagePassword}</p>
      </div>
      <div class="flex items-center justify-between">
        <button on:click={handleLogin} class="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="button">
            Sign In
        </button>
        <a class="inline-block align-baseline font-bold text-sm text-purple-500 hover:text-purple-800" href="#">
          Forgot Password?
        </a>
      </div>
    </form>
  </div>