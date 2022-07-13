$('#stock-handler').validate({ 
    "rules": {
        "input__input--id": {
            required: true
        },
        "input__input--name": {
            required: true
        },
        "input__input--count": {
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
        "input__input--count": {
            required: 'Debe ingresar una cantidad',
            number: 'Debe ingresar un número'
        },
        "img__input": {
            required: 'Debe seleccionar una imágen'
        }
    }
});

// Validadores

$.validator.addMethod(
    "validateMin",
    (value, validate) => {
        if (validate) {
            return value >= 0;
        }
    },
    "El campo debe ser mayor igual a 0"
);

$("#input__input--count").rules("add", { validateMin: true });