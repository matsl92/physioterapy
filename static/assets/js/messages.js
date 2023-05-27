const messages = document.querySelectorAll('[data-notify="container"]');

var i;
messages.forEach(message => {
    i = message.querySelector('button i');
    i.addEventListener('click', () => {
        message.classList.add('fadeOutUp');
        console.log('i was clicked')
    })

    setTimeout(() => {
        message.classList.add('fadeOutUp');
    }, 18000)

    setTimeout(() => {
        message.remove();
    }, 20000)
})