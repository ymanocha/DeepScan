document.addEventListener("DOMContentLoaded", ()=>{
    const form = document.getElementById("signupForm")
    form.addEventListener("submit", async(e)=>{
        e.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();
        
        if (!name || !email || !password){
            alert("Please fill in all fields");
            return;
        }

        try{
            const res = await fetch("/auth/signup",{
                method: "POST",
                headers:{
                    "Content-Type":"application/json",
                },
                body: JSON.stringify({ name, email, password})
            });

            const data = await res.json();

            if (res.ok){
                alert("Signup Succesful!, Please log in to continue")
                window.location.href = "/login";
            }
            else {
                alert(data.detail || "Signup Failed. Please try again")
            }
        }
        catch(error){
            console.error("Error during signup", error);
            alert("Something went wrong. Please try again later. ");
        }

    
        })


    


})  