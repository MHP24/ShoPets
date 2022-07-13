const cart = document.querySelector('.modalcart');

let products = [];
let count = 0;

const addToCart  = (e) => {
    let productEvent = e.target.closest('.product');
    let counterDesk = document.querySelector('.cart__count--mob');
    let counterMob = document.querySelector('.cart__count--desk');

    const product = {
        img: productEvent.querySelector('.img__src').src,
        name: productEvent.querySelector('.description__name').textContent,
        price: productEvent.querySelector('.description__price').textContent,
    }
    products.push(product);
    count++;
    counterDesk.innerHTML = `<p class="cart__number">${count}</p>`;
    counterMob.innerHTML = `<p class="cart__number">${count}</p>`;
}

const add = (btn) => {
    let item = btn.closest('.item__counter');
    item.querySelector('.counter__count').value = parseInt(item.querySelector('.counter__count').value) + 1;
}

const min = (btn) => {
    let item = btn.closest('.item__counter');
    let val = parseInt(item.querySelector('.counter__count').value);
    if(val >= 1) {
        item.querySelector('.counter__count').value =  val - 1;
    }
}

const showCart = (products) => {
    let productList = '';
    let totalPrice = 0;
    let productCount = 0;
    products.forEach( ({img, name, price}) => {
        totalPrice += parseInt(price.replace('$', ''));
        productCount ++;
        productList += `
        <div class="list__item">
            <img src="${img}" alt="product" class="item__img">
            <div class="item__description">
                <p class="description__title">${name}</p>
            </div>

            <div class="item__counter">
                <button class="counter__min" onclick = min(this)>-</button>
                <input type="number" name="counter__count" class="counter__count" id="count" value=1>
                <button class="counter__add" onclick = add(this)>+</button>
            </div>

            <p class="item__price">${price}</p>
        </div>
        `;
    });

    let summary = `
        <div class="summary__item">
            <div class="summary__count">
                <p>${productCount} Producto(s)</p>
            </div>
            <label>C&oacute;digo de descuento</label>
            <input type="text" value="C4D0GS" name="discountcode" class="summary__code" id="discount">
        </div>

        <div class="summary__item">
            <p id="total">Total $${totalPrice}CLP</p>
            <p id="total-price">Precio $${totalPrice * 0.5}CLP</p>
            <button class="summary__btn">Ir a Pagar</button>
        </div>
    `;

    document.getElementById('summary__payment').innerHTML = summary;
    document.querySelector('.cart__list').innerHTML = productList;
    cart.classList.toggle('showCart');
}

const btns  = document.querySelectorAll('.product__btn');
btns.forEach(btn => {
    btn.addEventListener('click', addToCart);
})

document.getElementById('nav__cart').addEventListener('click', () => {
    showCart(products);
});

// Tablet - Mobile
document.getElementById('nav__cart--f').addEventListener('click', () => {
    showCart(products);
});

document.getElementById('closeCart').addEventListener('click', () => {
    cart.classList.remove('showCart');
});
