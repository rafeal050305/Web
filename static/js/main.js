function toggleMobileMenu() {
  const mobileMenu = document.getElementById("mobileMenu");
  const toggleButton = document.querySelector(".mobile-menu-toggle i");

  mobileMenu.classList.toggle("active");

  if (mobileMenu.classList.contains("active")) {
    toggleButton.classList.remove("fa-bars");
    toggleButton.classList.add("fa-times");
  } else {
    toggleButton.classList.remove("fa-times");
    toggleButton.classList.add("fa-bars");
  }
}

// Cerrar menú móvil al hacer clic en un enlace
document.querySelectorAll(".mobile-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    const mobileMenu = document.getElementById("mobileMenu");
    const toggleButton = document.querySelector(".mobile-menu-toggle i");

    mobileMenu.classList.remove("active");
    toggleButton.classList.remove("fa-times");
    toggleButton.classList.add("fa-bars");
  });
});
