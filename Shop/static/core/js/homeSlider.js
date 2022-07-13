let slides = document.querySelectorAll('.slider__item');
let btns = document.querySelectorAll('.slider__btn');
let currentSlide = 1;

//Manual
const navigate = (index) => {
    slides.forEach((slide) => {
        slide.classList.remove('slider--active');

        btns.forEach(btn => {
            btn.classList.remove('slider--active');
        });
    })
    slides[index].classList.toggle('slider--active')
    btns[index].classList.toggle('slider--active');
};

btns.forEach((btn, i) => {
  // console.log(i)
  // console.log(btn)
    btn.addEventListener("click", () => {
        navigate(i);
    });

    currentSlide = i;
});


//AutoRepeat

const autoRepeat = () => {
    let active = document.getElementsByClassName('slider--active');
    let i = 1;

    const repeater = () => {
      setTimeout(() => {
        [...active].forEach((activeSlide) => {
          activeSlide.classList.remove('slider--active');
        });

        slides[i].classList.toggle('slider--active');
        btns[i].classList.toggle('slider--active');
        i++;

        if(slides.length === i){
          i = 0;
        }
        repeater();
      }, 6000);
    }
    repeater();
}
autoRepeat();
