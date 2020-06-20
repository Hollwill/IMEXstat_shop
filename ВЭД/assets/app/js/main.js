$(function ()    {
    $(document).ready(function(){
        $("#navbarTogglerDemo02").on("click","a", function (event) {
            $("#navbarTogglerDemo02").removeClass('show');
        });
    });
    $(document).ready(function(){
        $("#header__menu, #header__menu-mobile, #welcome__arrow, #welcome__text, #footer").on("click","a", function (event) {
            event.preventDefault();
            var id  = $(this).attr('href'),
                top = $(id).offset().top;
            $('body,html').animate({scrollTop: top-100}, 1500);
        });
    });
    $(document).ready(function(){
        $(window).scroll(function(){
            if($(window).scrollTop()>250){
                $('#up').fadeIn(900)
            }else{
                $('#up').fadeOut(700)
            }
        });
    });
});

function cartBuy(a,a1,b,b1) {
    document.getElementById(a).style.display = "flex";
    document.getElementById(a1).style.display = "flex";
    document.getElementById(b).style.display = "none";
    document.getElementById(b1).style.display = "none";
}
function lkExtend(a) {
    var elem = document.querySelector(a)
    elem.classList.toggle("lkExtendDN");
}
function changeText (a) {
    var id = a.id;
    var text = a.innerText;
    if (text=="Смотреть ещё") {
        a.innerText="Свернуть";
    }
    if (text=="Свернуть") {
        a.innerText="Смотреть ещё";
    }
}
