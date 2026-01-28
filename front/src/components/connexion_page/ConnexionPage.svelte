<script>
    import Login from './Login.svelte';
    import { user } from "../../stores/user";
    export let isLogged = false;
    export let status = "idle";

    let username = "";
    let password = "";

    async function handleLogin() {
  
        const response = await fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json", 
            },
            // credentials: "include", // REQUIRED for cookies
            body: JSON.stringify({
                email: username,
                password: password
            })
        });

        const data = await response.json();
        if (data.success) {
            status = "success";
            console.log("Logged in Successfully", username, password);
            isLogged = true;
            user.set(data.user.email);
            if (typeof localStorage !== "undefined") {
                localStorage.setItem("loggedIn", "true");
                localStorage.setItem("user", data.user.email.toUpperCase());
            }
            window.location.href = "/";
        } else {
            status = "error";
            console.log("Logged in Failed", username, password);
            return;
        }
    }
    


</script>
<h1 class="w-full mb-20 text-3xl sm:text-5xl md:text-7xl font-bold">
    <span class="underline underline-offset-[24px]">Welcome</span> to AdAlytics.
</h1>
<div class="w-full flex justify-center h-screen">
    <Login bind:username bind:password handleLogin={handleLogin} status={status}/>
</div>