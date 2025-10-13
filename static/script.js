document.getElementById("uploadForm").addEventListener("submit", async (e)=>{
    e.preventDefault();
    const fileInput = document.getElementById("video-upload");
    const file = fileInput.files[0];
    if(!file) return alert("please choose a file first!")

    const formData = new FormData();
    formData.append("file",file);

    try{
        const response = await fetch("/api/detect", {
            method:"POST",
            body:formData
        });
        const data = await response.json();
        console.log(data);
    } catch (err) {
        console.log(err);
        alert("Error Uploading File")
    }
     

});