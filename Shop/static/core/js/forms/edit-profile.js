$('#edit-profile').validate({ 
    "rules": {
        "input__input--name": {
            required: true
        },
        "input__input--email": {
            required: true,
            email: true,
        },
        "input__input--password": {
            required: true,
            minlength : 10,
        },
        "input__input--password2": {
            required: true,
            minlength : 10,
            equalTo : "#input__input--password",
        },
        "input__input--img": {
            required: true
        }
    },
    messages: {
        "input__input--name": {
            required: 'Debe ingresar sus nombres'
        },
        "input__input--email": {
            required: 'Debe ingresar su correo electrónico',
            email: 'Formato de correo incorrecto'
        },
        "input__input--password": {
            required: 'Debe ingresar una contraseña',
            minlength: 'La mínima cantidad de carácteres de la contraseña es 10'
        },
        "input__input--password2": {
            required: 'Debe repetir la misma contraseña',
            minlength: 'La mínima cantidad de carácteres de la contraseña es 10',
            equalTo: 'La repetición de contraseña debe coincidir con la contraseña original'
        },
        "input__input--img": {
            required: 'Debe Adjuntar una imágen'
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

$.validator.addMethod(
    "oneNumber",
    (value, validate) => {
        if (validate) {
            let re = new RegExp('.*[0-9].*');
            let resp = re.test(value);
            return resp;
        }
    },
    "La contraseña debe contener al menos un número"
);

$.validator.addMethod(
    "oneMayus",
    (value, validate) => {
        if (validate) {
            let re = new RegExp('.*[A-Z].*');
            let resp = re.test(value);
            return resp;
        }
    },
    "La contraseña debe contener al menos una mayúscula"
);

// Asignaciones
$("#input__input--email").rules("add", { validateMail: true });
$("#input__input--password").rules("add", { oneNumber: true });
$("#input__input--password").rules("add", { oneMayus: true });