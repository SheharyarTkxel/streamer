// Change the text of custom file uploader
const actualBtn = document.getElementById('actual-btn');
const fileChosen = document.getElementById('file-chosen');
actualBtn.addEventListener('change', function(){
  fileChosen.textContent = this.files[0].name
})


// It checks either file uploaded by user is SRT or not.
function validation() {
  const filePath = document.getElementById("actual-btn").value;
  const fileName = filePath.split(/(\\|\/)/g).pop();
  const extension = fileName.split('.').slice(-1)[0]

  if(extension != 'srt'){
    document.getElementById("msg").innerHTML = "Please Upload SRT file";
    return false;
  }
}


// When process of updating the SRT file completes, then this function disables the loader.
function loaderFunction(){
    const loader = document.getElementById("loading");
	loader.style.display = 'none';
};
