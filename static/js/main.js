AOS.init();

let nav = document.querySelector("nav");
window.onscroll = function () {
  if (document.documentElement.scrollTop > 100) {
    nav.classList.add("navbar-scroll");
  }
  else {
    nav.classList.remove("navbar-scroll");
  }
}


