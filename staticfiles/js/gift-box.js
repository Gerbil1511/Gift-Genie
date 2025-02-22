const click = document.querySelector('.gift-container');
const lid = document.querySelector('.lid');
const giftBox = document.querySelector('.gift-box');
const shadow = document.querySelector('.shadow');
const surprise = document.querySelector('.surprise');
const text = document.querySelector('.text');

click.addEventListener('click', () => {
    if (click.className === "gift-container") {
        click.classList.add('active');
        lid.classList.add('active');
        giftBox.classList.add('active');
        shadow.classList.add('active');
        surprise.classList.add('active');
        text.classList.add('active');
    } else {
        click.classList.remove('active');
        lid.classList.remove('active');
        giftBox.classList.remove('active');
        shadow.classList.remove('active');
        surprise.classList.remove('active');
        text.classList.remove('active');
       
    }
});
