const messages = document.querySelectorAll('[data-notify="container"]');

var i;
messages.forEach(message => {
    i = message.querySelector('button i');
    i.addEventListener('click', () => {
        message.classList.add('fadeOutUp');
    })

    setTimeout(() => {
        message.classList.add('fadeOutUp');
    }, 10000)

    setTimeout(() => {
        message.remove();
    }, 12000)
})