window.onload = function () {
    const input = document.getElementById("title");
    if (input) {
        input.focus();

        input.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                this.form.submit();
            }
        });
    }

    const toggles = document.querySelectorAll(".read-more");
    toggles.forEach(btn => {
        btn.addEventListener("click", () => {
            const overview = btn.previousElementSibling;
            overview.classList.toggle("expanded");
            btn.textContent = overview.classList.contains("expanded") ? "Read less" : "Read more";
        });
    });
};
