// Add scroll event to shrink and move logo when scrolling
window.addEventListener("scroll", function() {
    let logoContainer = document.getElementById("logoContainer");

    if (window.scrollY > 50) {
        document.body.classList.add("scrolled");
    } else {
        document.body.classList.remove("scrolled");
    }
});
