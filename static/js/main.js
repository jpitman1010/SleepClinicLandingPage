$(document).ready(function(){

    $('.fa-bars').click(function() {
        $(this).toggleClass('fa-times');
        $('.nav').toggleClass('nav-toggle');
    });

    $(window).on('load scroll', function() {
        $('.fa-bars').removeClass('fa-times');
        $('.nav').removeClass('nav-toggle');
    });

    if($(window).scrollTop() > 10){
        $('header').addClass('header-active');
    }else{
        $('header').removeClass('header-active');
    }

    $('#facility').magnificPopup({
        delegate:'a',
        type:'image',
        // closeOnContentClick: true, 
        gallery:{
            enabled: true
        }
    });

});


var data = new FormData();
jQuery.each(jQuery('#file')[0].files,function(i, file) {
    data.append('file-'+i, file);
});

jQuery.ajax({
    url: 'php/upload.php',
    data: data,
    cache: false,
    contentType: false,
    processData: false,
    type: 'POST',
    success: function(data){
        alert(data);
    }
});



// function phonenumber(){
//     let phone = document.forms["form"]["phone"].value;
//     let phoneNumber = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
//     if(phone.match(phoneNumber)){
//         return true;
//         }
//     else
//         {
//         alert("Please enter a valid phone number");
//         return false;
//         }
// }


// function validateForm() {
//     let firstName = document.forms["form"]["fname"].value;
//     let lastName = document.forms["form"]["lname"].value;
//     let phone = document.forms["form"]["phone"].value;
//     // let timeSelection = document.forms["form"]["times"].value;

//     if (firstName == "") {
//       alert("First name must be filled out");
//       return false;
//     }
//     if (lastName == "") {
//         alert("Last name must be filled out");
//         return false;
//       }
//     if (phone == "") {
//         alert("Phone number must be filled out");
//         return false;
//     }

//     phoneNumber()

// }

// function submitForm() {
//     if (validateForm() !== false) {
//     alert("Your information has successfully been submitted to our scheduling team.  We look forward to speaking with you.");
//     }
// }



const fname = document.querySelector('#fname');
const lname = document.querySelector('#lname');
const phone = document.querySelector('#phone');
const email = document.querySelector('#email');

const form = document.querySelector('#submit');


const checkFirstName = () => {

    let valid = false;

    const min = 3,
        max = 25;

    const fname = fname.value.trim();

    if (!isRequired(fname)) {
        showError(fname, 'First name cannot be blank.');
    } else if (!isBetween(fname.length, min, max)) {
        showError(fname, `First name must be between ${min} and ${max} characters.`)
    } else {
        showSuccess(fname);
        valid = true;
    }
    return valid;
};

const checkLastName = () => {

    let valid = false;

    const min = 3,
        max = 25;

    const lname = lname.value.trim();

    if (!isRequired(lname)) {
        showError(lname, 'Last name cannot be blank.');
    } else if (!isBetween(lname.length, min, max)) {
        showError(lname, `Last name must be between ${min} and ${max} characters.`)
    } else {
        showSuccess(lname);
        valid = true;
    }
    return valid;
};


const checkEmail = () => {
    let valid = false;
    const email = email.value.trim();
    if (!isRequired(email)) {
        showError(email, 'Email cannot be blank.');
    } else if (!isEmailValid(email)) {
        showError(email, 'Email is not valid.')
    } else {
        showSuccess(email);
        valid = true;
    }
    return valid;
};

const isEmailValid = (email) => {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
};


const checkPhone = () => {
    let valid = false;
    const phone = phone.value.trim();
    if (!isRequired(phone)) {
        showError(phone, 'Phone number cannot be blank.');
    } else if (!isPhoneValid(phone)) {
        showError(phone, 'Phone number is not valid.')
    } else {
        showSuccess(phone);
        valid = true;
    }
    return valid;
};


const isPhoneValid = (phone) => {
    const re = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
    return re.test(phone);
};

const isRequired = value => value === '' ? false : true;
const isBetween = (length, min, max) => length < min || length > max ? false : true;


const showError = (input, message) => {
    // get the form-field element
    const formField = input.parentElement;
    // add the error class
    formField.classList.remove('success');
    formField.classList.add('error');

    // show the error message
    const error = formField.querySelector('small');
    error.textContent = message;
};

const showSuccess = (input) => {
    // get the form-field element
    const formField = input.parentElement;

    // remove the error class
    formField.classList.remove('error');
    formField.classList.add('success');

    // hide the error message
    const error = formField.querySelector('small');
    error.textContent = '';
}


form.addEventListener('submit', function (e) {
    // prevent the form from submitting
    e.preventDefault();

    // validate fields
    let isFirstNameValid = checkFirstName(),
        isLastNameValid = checkLastName(),
        isEmailValid = checkEmail(),
        isPhoneValid = checkPhone()

    let isFormValid = isUsernameValid &&
        isEmailValid &&
        isPasswordValid &&
        isConfirmPasswordValid;

    // submit to the server if the form is valid
    if (isFormValid) {

    }
});


const debounce = (fn, delay = 500) => {
    let timeoutId;
    return (...args) => {
        // cancel the previous timer
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        // setup a new timer
        timeoutId = setTimeout(() => {
            fn.apply(null, args)
        }, delay);
    };
};

form.addEventListener('input', debounce(function (e) {
    switch (e.target.id) {
        case 'username':
            checkUsername();
            break;
        case 'email':
            checkEmail();
            break;
        case 'password':
            checkPassword();
            break;
        case 'confirm-password':
            checkConfirmPassword();
            break;
    }
}));







