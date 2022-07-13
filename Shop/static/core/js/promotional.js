const loadData = url => {
    fetch(url)
    .then(response => response.json())
    .then(data => {
        let elements = '';
        data.forEach( ( { id, title, price, category, image } ) => {
            elements += `
                <li id="p-${id}" class="product">
                    <div class="product__img">
                        <img src="${image}" alt="" class="img__src">
                    </div>
                    <div class="product__description">
                        <p class="description__company">${category}</p>
                        <p class="description__name">${title}</p>
                        <p class="description__price">$${price}</p>
                    </div>
                </li>
            `;
        });

        document.getElementById('clothes__container').innerHTML = elements;
    })
    .catch(err => console.log(err));
}


loadData(`http://fakestoreapi.com/products`);