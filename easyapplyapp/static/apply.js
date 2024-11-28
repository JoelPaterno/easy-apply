var collapsible = document.getElementsByClassName("collapsible");
var i;

for (i = 0; collapsible.length; i++) {
    collapsible[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var content = this.nextElementSibling;
        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
    });
};

function loading() {
    let applyform = document.getElementById('applyform');
    let container = document.createElement('div');
    container.className = "loading-div";
    let img = document.createElement('img');
    img.id = "loading-img";
    let loadingText = document.createElement('p');
    img.src = "https://easyapply.joelpaterno.tech/static/feather-solid.svg";
    loadingText.innerHTML = "Please Wait (20 - 30 seconds) while your Job Application is Prepared...";
    container.appendChild(loadingText);
    container.appendChild(img);
    applyform.after(container);
    console.log(container.outerHTML);
};