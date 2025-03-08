async function processText() {
    const generateBtn = document.querySelector('.generate-btn');
    const text = document.getElementById("textInput").value;
    if (!text) {
        alert("Please enter some text to generate an infographic.");
        return;
    }
    generateBtn.disabled = true; // Disable button immediately

    // Send request to generate the image
    const generateResponse = await fetch("http://127.0.0.1:8000/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });
    const generateData = await generateResponse.json();
    const jobId = generateData.job_id;

    // Update the UI with a process start message (centered)
    document.getElementById("output").innerHTML = `
      <div class="status-container">
        <div class="status-message">Processing, please wait...</div>
      </div>
    `;

    // Function to check the status of the process
    async function checkStatus() {
        const statusResponse = await fetch(`http://127.0.0.1:8000/api/status/${jobId}`);
        const statusData = await statusResponse.json();

        // Update status in the same centered container
        document.getElementById("output").innerHTML = `
          <div class="status-container">
            <div class="status-message">Status: ${statusData.status}</div>
          </div>
        `;
        
        if (statusData.status === "completed") {
            // When the process is complete, request the final results
            const resultResponse = await fetch(`http://127.0.0.1:8000/api/result/${jobId}`);
            const resultData = await resultResponse.json();

            // Ensure we only proceed if the job truly completed
            if (resultData.status === "completed") {
                const { result } = resultData;

                let imagesHtml = "";
                for (const [lang, filename] of Object.entries(result)) {
                  imagesHtml += `
                    <div class="infographic-item">
                      <h3>${lang} Infographic</h3>
                      <img src="${filename}?v=${Date.now()}" alt="Infographic">
                      <button class="download-btn" onclick="downloadImage('${filename}', '${lang}')">Download ${lang}</button>
                    </div>`;
                }

                // Replace status with the final images
                document.getElementById("output").innerHTML = imagesHtml;

            } else {
                document.getElementById("output").innerHTML = `
                  <div class="status-container">
                    <div class="status-message">${resultData.status}</div>
                  </div>
                `;
            }

            generateBtn.disabled = false; // Re-enable button after completion

        } else if (statusData.status.startsWith("error")) {
            // Show error in the same centered container
            document.getElementById("output").innerHTML = `
              <div class="status-container">
                <div class="status-message">${statusData.status}</div>
              </div>
            `;
            generateBtn.disabled = false; // Re-enable button if error occurs

        } else {
            // If still processing, check again after 3 seconds
            setTimeout(checkStatus, 2000);
        }
    }
    
    // Start checking the process status
    checkStatus();
}

function downloadAllImages() {
    const images = document.querySelectorAll('#output img');
    images.forEach((img, index) => {
      const link = document.createElement('a');
      link.href = img.src;
      link.download = `infographic_${index + 1}.svg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
}

function downloadImage(url, lang) {
    const a = document.createElement('a');
    a.href = url;
    a.download = `${lang}_infographic.svg`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
