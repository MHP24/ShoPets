
//Navigation

const btnMenu = document.getElementById('menu');
const nav = document.querySelector('.navigation__indexs');
const buttons = document.querySelector('.nav__buttons');
btnMenu.addEventListener('click', () => {
    nav.classList.toggle('navigation--show');
    // console.log('clciked');
});

window.addEventListener("click", w => {
    // console.log(w.target);
    if(nav.classList.contains("navigation--show") && w.target != document.querySelector(".nav__item")
    && w.target != document.querySelector("#menu__icon")
    && w.target != document.querySelector(".navigation")) {
        nav.classList.toggle("navigation--show");
    }
});
