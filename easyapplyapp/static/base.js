const hamburger = document.getElementsByClassName("hamburger")[0];
const navlinks = document.getElementsByClassName("nav-links")[0];
let menuOpen = false;

hamburger.addEventListener('click', () => {
    console.log("hamburger clicked");
    console.log(menuOpen);
    if (menuOpen == false) {
        navlinks.style.display = "block";
        menuOpen = true;
    }
    else if (menuOpen == true) {
        navlinks.style.display = "none";
        menuOpen = false;
    }
});