
//Navigation

const btnMenu = document.getElementById('searcher__burger');
const nav = document.querySelector('.dashboard-navigation');
const buttons = document.querySelector('.nav');
btnMenu.addEventListener('click', () => {
    nav.classList.toggle('dashboard-navigation--show');
    // console.log('clciked');
});

window.addEventListener("click", w => {
    // console.log(w.target);
    if(nav.classList.contains("dashboard-navigation--show") && w.target != document.querySelector(".nav__item")
    && w.target != document.querySelector(".nav__name")
    && w.target != document.querySelector(".nav__navigation")
    && w.target != document.querySelector(".dashboard-navigation")
    && w.target != document.querySelector("#searcher__burger")) {
        nav.classList.toggle("dashboard-navigation--show");
    }
});
