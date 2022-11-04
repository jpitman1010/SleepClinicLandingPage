const openModalButtons = document.querySelectorAll('[data-target]')
const closeModalButtons = document.querySelectorAll('[data-dismiss]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
})


closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})


function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    console.log('modal should be open')
}



function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
}

