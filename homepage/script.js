var color = 1;

function toggle() {
    var body = document.querySelector("body");
    var text = document.querySelector("#modo");
    if (color == 1) {
        body.style.background = "linear-gradient(153deg, rgba(255,255,255,1) 31%, rgba(138,130,130,1) 65%)";
        text.innerHTML = "Dark Mode";
    }
    else {
        body.style.background = "linear-gradient(150deg, rgba(0,0,0,1) 31%, rgba(0,2,27,1) 100%)";
        text.innerHTML = "Light Mode";
    }


    color *= -1;
}