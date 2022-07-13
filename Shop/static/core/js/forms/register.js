$('#register').validate({ 
    "rules": {
        "input__input--rut": {
            required: true
        },
        "input__input--names": {
            required: true
        },
        "input__input--lastnames": {
            required: true
        },
        "input__input--email": {
            required: true,
            email: true,
        },
        "input__input--adress": {
            required: true,
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
    },
    messages: {
        "input__input--rut": {
            required: 'Debe ingresar un RUT válido'
        },
        "input__input--names": {
            required: 'Debe ingresar sus nombres'
        },
        "input__input--lastnames": {
            required: 'Debe ingresar sus apellidos'
        },
        "input__input--email": {
            required: 'Debe ingresar su correo electrónico',
            email: 'Formato de correo incorrecto'
        },
        "input__input--adress": {
            required: 'Debe ingresar su dirección',
        },
        "input__input--password": {
            required: 'Debe ingresar una contraseña',
            minlength: 'La mínima cantidad de carácteres de la contraseña es 10'
        },
        "input__input--password2": {
            required: 'Debe repetir la misma contraseña',
            minlength: 'La mínima cantidad de carácteres de la contraseña es 10',
            equalTo: 'La repetición de contraseña debe coincidir con la contraseña original'
        }
    }
});

const validateEmail = (email) => {
    let re = /\S+@\S+\.\S+/;
    return re.test(email);
}

const dv = (T) => {
    let M=0,S=1;
    for(; T; T = Math.floor(T/10))
        S=(S + T % 10 * (9 - M++ %6))%11;
    return S?S-1:'k';
}

const validateRut = (fullRut) => {
    if (!/^[0-9]+-[0-9kK]{1}$/.test(fullRut)) {
        return false;
    }
    let tmp = fullRut.split('-');
    let rut = tmp[0];
    let digv = tmp[1]; 
    if (digv == 'k') digv = 'K' ;
    return (dv(rut) == digv );
}

// Validadores
$.validator.addMethod(
    "validateRut",
    (value, validate) => {
        if (validate) {
            return validateRut(value);
        }
    },
    "El formato del rut no es válido"
);

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
$("#input__input--rut").rules("add", { validateRut: true });
$("#input__input--password").rules("add", { oneNumber: true });
$("#input__input--password").rules("add", { oneMayus: true });