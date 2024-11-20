document.querySelectorAll(
    ".slide-up, .slide-RtL, .slide-LtR"
).forEach((el) => {
    new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting && entry.target.classList.contains("slide-up")) {
                entry.target.classList.add("show-slide-up");
            } else if (
                entry.isIntersecting &&
                entry.target.classList.contains("slide-RtL")
            ) {
                entry.target.classList.add("show-slide-RtL");
            } else if (
                entry.isIntersecting &&
                entry.target.classList.contains("slide-LtR")
            ) {
                entry.target.classList.add("show-slide-LtR");
            }
        });
    }).observe(el);
});