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
            const card = btn.closest(".card");
            if (!card) return;

            card.classList.toggle("expanded");

            const overview = card.querySelector(".overview");
            const isExpanded = card.classList.contains("expanded");
            btn.textContent = isExpanded ? "Read less" : "Read more";
        });
    });
};
