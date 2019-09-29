$(function ()    {
    $(document).ready(function(){
        $("#navbarTogglerDemo02").on("click","a", function (event) {
            $("#navbarTogglerDemo02").removeClass('show');
        });
    });

    /*Нерабочий код*/
    /*
    $(document).ready(function(){
        $("#header__menu, #header__menu-mobile, #welcome__arrow, #welcome__text, #footer").on("click","a", function (event) {
            event.preventDefault();
            var id  = $(this).attr('href'),
                top = $(id).offset().top;
            $('body,html').animate({scrollTop: top-100}, 1500);
        });
    });*/
    $(document).ready(function(){
        $(window).scroll(function(){
            if($(window).scrollTop()>250){
                $('#up').fadeIn(900)
            }else{
                $('#up').fadeOut(700)
            }
        });
    });
    /*-------------------------------------------------
    На основе url меняет цвет нужного типа исследования 
    -------------------------------------------------*/
    $(document).ready(function(){
        if (window.location.href.indexOf('research=') >= 0) {
            $('.ready__type-item').className = 'ready__type-item';
        } else {
            if (window.location.href.indexOf('industry') >= 0) {
                $('#industry').addClass('ready__type-itemActive'); 
            } else if (window.location.href.indexOf('export') >= 0) {
                $('#export').addClass('ready__type-itemActive');
            } else if (window.location.href.indexOf('import') >= 0) {
                $('#import').addClass('ready__type-itemActive');
            }
        }
    });
    $(document).ready(function(){
        if (window.location.href.indexOf('settings') >= 0) {
            $('#lk_settings').addClass('lk__menu-activeItem')
        } else if (window.location.href.indexOf('favorite') >= 0) {
                $('#lk_favorite').addClass('lk__menu-activeItem');
        } /*else if (window.location.href.indexOf('export') >= 0) {
                $('#export').addClass('ready__type-itemActive');
        } else if (window.location.href.indexOf('export') >= 0) {
                $('#export').addClass('ready__type-itemActive');
        } else if (window.location.href.indexOf('export') >= 0) {
                $('#export').addClass('ready__type-itemActive');
        } else if (window.location.href.indexOf('export') >= 0) {
                $('#export').addClass('ready__type-itemActive');
        }*/
    });

    /*----------------------------------------------------------------------------
    На странице описания исследования показывать и скрывать контент в нижней части 
    в зависимости от выбора.
    ----------------------------------------------------------------------------*/
    $(document).ready(function(){
        $('#contents_button').on('click', function (event) {
            $('.ready__type-item').removeClass('ready__type-itemActive');
            $('#contents_button').addClass('ready__type-itemActive');
            $('.readyInner__text').hide();
            $('#contents').show();
        });
        $('#using_methods_button').on('click', function (event) {
            $('.ready__type-item').removeClass('ready__type-itemActive');
            $('#using_methods_button').addClass('ready__type-itemActive');
            $('.readyInner__text').hide();
            $('#using_methods').show();
        });
        $('#data_sources_button').on('click', function (event) {
            $('.ready__type-item').removeClass('ready__type-itemActive');
            $('#data_sources_button').addClass('ready__type-itemActive');
            $('.readyInner__text').hide();
            $('#data_sources').show();
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
