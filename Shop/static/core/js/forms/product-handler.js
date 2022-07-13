$('#product-handler').validate({ 
    "rules": {
        "input__input--id": {
            required: true
        },
        "input__input--name": {
            required: true
        },
        "input__input--description": {
            required: true,
            minlength: 10
        },
        "input__input--price1": {
            required: true,
            number: true
        },
        "input__input--discount": {
            required: true,
            number: true
        },
        "input__input--discount2": {
            required: true,
            number: true
        },
        "img__input": {
            required: true
        }
    },
    messages: {
        "input__input--id": {
            required: 'Debe ingresar un ID'
        },
        "input__input--name": {
            required: 'Debe ingresar un nombre para el producto'
        },
        "input__input--description": {
            required: 'Debe ingresar una descripción',
            minlength: 'Debe ser de mínimo 10 carácteres la descripción'
        },
        "input__input--price1": {
            required: 'Debe ingresar un valor',
            number: 'Debe ingresar un número válido'
        },
        "input__input--discount": {
            required: 'Debe ingresar un descuento',
            number: 'Debe ingresar un número válido'
        },
        "input__input--discount2": {
            required: 'Debe ingresar un descuento',
            number: 'Debe ingresar un número válido'
        },
        "img__input": {
            required: "Debe seleccionar una imágen"
        }
    }
});


$.validator.addMethod(
    "validateMin",
    (value, validate) => {
        if (validate) {
            return value >= 0;
        }
    },
    "El campo debe ser mayor igual a 0"
);

$("#input__input--price1").rules("add", { validateMin: true });
$("#input__input--discount").rules("add", { validateMin: true });
$("#input__input--discount2").rules("add", { validateMin: true });