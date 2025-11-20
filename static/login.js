document.addEventListener("DOMContentLoaded",()=>{
    const form = document.getElementById("loginForm");

    form.addEventListener("submit", async(e)=>{
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if(!email || !password){
            alert("Please fill in all details");
            return;
        }

        try{
            const res = await fetch("api/auth/login",{
              method: "POST",
              headers: {"Content-Type":"application/json"},
              body: JSON.stringify({ email, password}),
            });

            const data = await res.json();

            if (res.ok){
                localStorage.setItem("token", data.access_token);
                alert("Login succesful!");

                window.location.href = "/";
            } 
            else{
                alert(data.detail || "Invalid email or password.");
            }
        }catch(error){
           console.error("Login error:", err);
           alert("Something went wrong. Please try again.");
        }
    })
})