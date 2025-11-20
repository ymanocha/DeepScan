document.addEventListener("DOMContentLoaded", ()=>{
     const uploadSection = document.getElementById("upload-section");
     const resultSection = document.getElementById("result-section");
     const fileInput = document.getElementById("file-input");
     // const fileNameEl = document.getElementById("file-name");
     //  const uploadBtn = document.getElementById("uploadBtn");
     const progressSection = document.getElementById("progress-section");
     const progressBar = document.getElementById("progress-bar");
     //  const resultCard = document.getElementById("result-card");
     const resultConfidence = document.getElementById("result-confidence");
     //  const statusText = document.getElementById("status-text");
     const resultLabel = document.getElementById("result-label");
     const limeImg = document.getElementById("lime-img");
     const tryAgainBtn = document.getElementById("try-again");
     const token = localStorage.getItem("token");
     const uploadBox = document.getElementById("upload-box");
    

// Prevent browser from opening the dropped file
   ["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
  uploadBox.addEventListener(eventName, e => {
    e.preventDefault();
    e.stopPropagation();
  });
});

// Highlight when file is dragged over
   ["dragenter", "dragover"].forEach(eventName => {
    uploadBox.addEventListener(eventName, () => {
    uploadBox.classList.add("drag-hover");
  });
});

// Remove highlight when dragging leaves
   ["dragleave", "drop"].forEach(eventName => {
    uploadBox.addEventListener(eventName, () => {
    uploadBox.classList.remove("drag-hover");
  });
});

// Handle dropped file
uploadBox.addEventListener("drop", e => {
  const files = e.dataTransfer.files;
  if (!files.length) return;

  fileInput.files = files;
  fileInput.dispatchEvent(new Event("change"));
});


     let simulateInterval = null;
      
     tryAgainBtn.addEventListener("click", () => {
     resultSection.classList.remove("active");
     uploadSection.classList.add("active");
     progressSection.classList.remove("active");
     progressBar.style.width = "0%";
     limeImg.classList.add("hidden");
     fileInput.value = "";
});

    function showError(msg) {
  stopSimulatedProgress();
  progressBar.style.width = "100%";
  progressBar.style.background = "linear-gradient(90deg,#ef4444,#b91c1c)";
  console.error(msg);
}

     function resetUI(){
        progressBar.style.width="0%";
        // statusText.textContent = "Analayzing video";
        progressSection.classList.remove("active");
        limeImg.classList.add("hidden");
        //uploadBtn.disabled=false;
     }

     function startSimulatedProgress(){
        let progressCounter = 0;
        progressBar.style.width="0%";
        progressSection.classList.add("active");
       // uploadBtn.disabled = true;

        simulateInterval = setInterval(()=>{
            const jump = Math.random()*4;
            progressCounter = Math.min(90,progressCounter+jump);
            progressBar.style.width=progressCounter+"%"},1200);
        }


    function stopSimulatedProgress(){
        if (simulateInterval){
            clearInterval(simulateInterval);
            simulateInterval=null;
        }
    }
     
    function showResult(body) {
        stopSimulatedProgress();
        progressBar.style.width = "100%";
        setTimeout(() => {
        progressSection.classList.remove("active");
        resultSection.classList.add("active");

     
      resultLabel.textContent = body.result || "UNKNOWN";
      resultConfidence.textContent =
        "Confidence: " + (body.confidence?.toFixed(2) + "%" || "N/A");

     
        if (body.lime_image) {
           limeImg.src = body.lime_image;
           limeImg.classList.remove("hidden");
 
        } else {
        limeImg.classList.add("hidden");
      }
    }, 500);
  }

    //if(body)
     
   // uploadBtn.disabled = false;
    
   fileInput.addEventListener("change",async()=>{
   const file = fileInput.files[0];
   if(!file) return alert("please choose a file first!")
     uploadSection.classList.remove("active");
     progressSection.classList.add("active");
     resultSection.classList.remove("active");
     startSimulatedProgress();

    try{
        const formdata = new FormData(); //
        formdata.append("file", file);
        
        const res = await fetch("/api/scans",{
            method: "POST",
            body: formdata,
            headers: token ? {Authorization: `Bearer ${token}`} : {}
        });
  

        if (!res.ok) {
            const errText = await res.text().catch(()=>"");
            showError(`Upload Failed: ${res.status} ${errText}`);
            return;
        }

        const body = await res.json();
        showResult(body);
    }
    catch(err){
        console.error(err);
    }
 


})


})
