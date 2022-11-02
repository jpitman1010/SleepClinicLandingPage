let request_appointment = document.getElementById("request-button");
let referral = document.getElementById("referral-button");
const contact_section = document.getElementById("contact");
const referral_section = document.getElementById("referrals");
const form_section = document.getElementById("form_section");


request_click = function () {
    if (contact_section.style.display === "none") {
        contact_section.style.display = "block";
        referral_section.style.display = "none";
        request_appointment.textContent = "Cancel";
        referral.textContent = "Send Referral"
    } else {
        contact_section.style.display = "none";
        referral_section.style.display = "none";
        request_appointment.textContent = "Request Appointment";

    }

}


referral_click = function () {
    if (referral_section.style.display === "none") {
        referral_section.style.display = "block";
        contact_section.style.display = "none";
        referral.textContent = "Cancel";
        request_appointment.textContent = "Request Appointment"
    } else {
        contact_section.style.display = "none";
        referral_section.style.display = "none";
        referral.textContent = "Send Referral";
    }
}



const openModalButtons = document.querySelectorAll('[data-target]')
const closeModalButtons = document.querySelectorAll('[data-dismiss]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
})


overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('.modal.active')
    modals.forEach(modal => {
        closeModal(modal);
    })
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})


function openModal(modal) {
    if(modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
    console.log('modal should be open')
}



function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}