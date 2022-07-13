$('#contact').validate({ 
    "rules": {
        "input__input--email": {
            required: true,
            email: true,
        },
        "input__input--name": {
            required: true,
        },
        "input__input--msg": {
            required: true,
            minlength: 10
        }
    },
    messages: {
        "input__input--email": {
            required: 'Debe ingresar su correo electrónico',
            email: 'Formato de correo incorrecto'
        },
        "input__input--name": {
            required: 'Debe ingresar su nombre',
        },
        "input__input--msg" : {
            required: 'Debe ingresar un mensaje',
            minlength: 'Debe tener mínimo 10 caracteres'
        }
    }
});

const validateEmail = (email) => {
    let re = /\S+@\S+\.\S+/;
    return re.test(email);
}

// Validadores
$.validator.addMethod(
    "validateMail",
    (value, validate) => {
        if (validate) {
            return validateEmail(value);
        }
    },
    "Formato de correo incorrecto"
);

// Asignaciones
$("#input__input--email").rules("add", { validateMail: true });