var slideIndex = 1;
pickSlide(slideIndex);
var autoInterval = setInterval(function(){ showSlide(slideIndex += 1); }, 2000);

function pickSlide(n) {
    slideIndex = n;
    showSlide(slideIndex);
    clearInterval(autoInterval);
}

function shiftSlide(n) {
    showSlide(slideIndex += n);
    clearInterval(autoInterval);
}

function showSlide(n) {
    var i;
    var slides = document.getElementsByClassName("slide");
    var controls = document.getElementsByClassName("slideshow-button");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length} ;
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        controls[i].className = controls[i].className.replace( 'active', '' );
    }
    slides[slideIndex-1].style.display = "block";
    controls[slideIndex-1].classList ? controls[slideIndex-1].classList.add('active') : controls[slideIndex-1].className += ' active';
}
