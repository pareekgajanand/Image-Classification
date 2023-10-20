const realFileBtn = document.getElementById("real-file");
const customButton = document.getElementById("custom-button");
const customTxt = document.getElementById("custom-text");
const uploadButton = document.getElementById("upload-button");

customButton.addEventListener("click", function () {
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function () {
    if (realFileBtn.value) {
        customTxt.innerHTML = realFileBtn.value;
        uploadButton.hidden = false;
    } else {
        customTxt.innerHTML = "No file chosen, yet.";
        uploadButton.hidden = true;
    }
});
