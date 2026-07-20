document.addEventListener("DOMContentLoaded", () => {
    const year = document.getElementById("current-year");
    if (year) year.textContent = new Date().getFullYear();

    const header = document.querySelector(".site-header");
    const setHeaderState = () => {
        if (header) header.classList.toggle("is-scrolled", window.scrollY > 10);
    };
    setHeaderState();
    window.addEventListener("scroll", setHeaderState, { passive: true });
});
