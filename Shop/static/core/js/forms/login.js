$('#login').validate({ 
    "rules": {
        "input__input--email": {
            required: true,
            email: true,
        },
        "input__input--password": {
            required: true,
        }
    },
    messages: {
        "input__input--email": {
            required: 'Debe ingresar su correo electrónico',
            email: 'Formato de correo incorrecto'
        },
        "input__input--password": {
            required: 'Debe ingresar una contraseña',
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