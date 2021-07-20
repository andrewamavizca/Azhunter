
function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
}


function checkbox() {

    var checkbox = document.getElementById("myCheck");
    if (checkbox.checked == true){
        container_main.style.display = "block";
        param_description.style.display="none";
    } else {
        container_main.style.display = "none";
        param_description.style.display="block";
    }

}

