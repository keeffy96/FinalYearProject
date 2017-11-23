function myFunction() {
    var x = document.getElementById("myDIV");
    var y = document.getElementById("moveJumbo");
    var z = document.getElementById("hideshow");
    var hide = document.getElementById('hideshow').className = "glyphicons glyphicons-minus"
    if (x.style.display === "none") {
        x.style.display = "block";
        y.style.width = "75%";
        z.className = "btn btn-default btn-lg";
        x.value = "Hide"       

    } else {
        x.style.display = "none";
        y.style.width = "100%";
        z.className = "btn btn-default btn-lg"
        z.value = "Show";
    }
}