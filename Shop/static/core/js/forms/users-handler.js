$('#users-handler').validate({ 
    "rules": {
        "input__input--id": {
            required: true
        },
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
        "usertype": {
            required: true
        },
        "input__input--profile-picture": {
            required: true
        }
    },
    messages: {
        "input__input--id": {
            required: 'Debe ingresar un ID'
        },
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
        "usertype": {
            required: "Debe seleccionar el tipo de usuario"
        },
        "input__input--profile-picture": {
            required: 'Debe seleccionar una imágen'
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

// Generador de contraseña
const generatePass = () => {
    let password = '';
    const uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const lowers = 'abcdefghijklmnopqrstuvwxyz';
    const numbers = '1234567890';
    const symbols = '!@#$%^&*()-_=+[]{};:,.<>/?|~ñ';
    
    for(let i = 0; i <=9; i++) {
        let randomLower = Math.floor(Math.random() * lowers.length);
        password += lowers.charAt(randomLower);
    }

    let randomUpper = Math.floor(Math.random() * uppers.length);
    password += uppers.charAt(randomUpper);

    let randomNumber = Math.floor(Math.random() * numbers.length);
    password += numbers.charAt(randomNumber);

    let randomSymbol = Math.floor(Math.random() * symbols.length);
    password += symbols.charAt(randomSymbol);

    return password;
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

const generateBtn = document.getElementById('generate-pass');
generateBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const inputPass = document.getElementById('input__input--password');
    const password = generatePass();
    // console.log(password);
    inputPass.value = password;
});