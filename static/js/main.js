// ======================================
// ALQARAWSHI RECRUITMENT
// Main JavaScript
// ======================================

// Initialize animations
AOS.init({
    duration: 900,
    once: true
});

// ==============================
// Mobile Sidebar
// ==============================

const menuBtn = document.getElementById("menu-btn");
const sidebar = document.getElementById("sidebar");

if (menuBtn && sidebar) {

    menuBtn.addEventListener("click", function () {

        sidebar.classList.toggle("show");

    });

}

// ==============================
// Animated Counter
// ==============================

const counters = document.querySelectorAll(".counter");

counters.forEach(counter => {

    counter.innerText = "0";

    const updateCounter = () => {

        const target = +counter.getAttribute("data-target");

        const current = +counter.innerText;

        const increment = target / 150;

        if (current < target) {

            counter.innerText = Math.ceil(current + increment);

            setTimeout(updateCounter, 15);

        } else {

            counter.innerText = target;

        }

    };

    updateCounter();

});

// ==============================
// Navbar Shadow
// ==============================

window.addEventListener("scroll", function () {
    const topbar = document.querySelector(".topbar");
    if (!topbar) return;
    if (window.scrollY > 30) {
        topbar.style.boxShadow = "0 8px 25px rgba(0,0,0,.18)";
    } else {
        topbar.style.boxShadow = "0 3px 10px rgba(0,0,0,.08)";
    }
});

// ==============================
// Back To Top
// ==============================

const topBtn = document.getElementById("topBtn");

if (topBtn) {

    window.addEventListener("scroll", function () {

        if (window.scrollY > 300)

            topBtn.style.display = "flex";

        else

            topBtn.style.display = "none";

    });

    topBtn.onclick = function () {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    };

}

// ==============================
// Card Animation
// ==============================

document.querySelectorAll(".card").forEach(card => {

    card.addEventListener("mouseenter", () => {

        card.style.transform = "translateY(-8px)";

    });

    card.addEventListener("mouseleave", () => {

        card.style.transform = "translateY(0px)";

    });

});

// ==============================
// Fade-in Sections
// ==============================

const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("visible");

        }

    });

});

document.querySelectorAll(".fade-section").forEach(section => {

    observer.observe(section);

});

// ==============================
// Loading Screen
// ==============================

window.onload = function () {

    const loader = document.getElementById("loader");

    if (loader) {

        loader.style.opacity = "0";

        setTimeout(() => {

            loader.style.display = "none";

        }, 500);

    }

};
