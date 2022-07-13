window.addEventListener('load', () => {
	new Glider(document.querySelector('.most-selled__products'), {
		slidesToShow: 1,
		slidesToScroll: 1,
		draggable: true,
		dots: '.most-selled__dots',
		arrows: {
		  prev: '.most-selled__btn--back',
		  next: '.most-selled__btn--next'
		},
		responsive: [
			{
			  breakpoint: 590,
			  settings: {
				slidesToShow: 2,
				slidesToScroll: 2,
				itemWidth: 150,
				duration: 0.25
			  }
			},{
			  breakpoint: 1000,
			  settings: {
				slidesToShow: 4,
				slidesToScroll: 4,
				itemWidth: 150,
				duration: 0.25
			  }
			}
		]
	  });
});