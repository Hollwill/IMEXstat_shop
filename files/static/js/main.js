$(function ()    {
    $(document).ready(function(){
        $("#navbarTogglerDemo02").on("click","a", function (event) {
            $("#navbarTogglerDemo02").removeClass('show');
        });
    });

    $('.accordion__title').each(function(){
            $(this).click(function(){
                $(this).toggleClass('active');
            });
        });

    $(document).ready(function(){
        $('#modal-thanx').modal('show');
    });

    $('.list-group-item_category').each(function(){
			$(this).click(function(e){
				e.preventDefault();
				$(this).toggleClass('active');
				$(this).siblings().removeClass('active');
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

function showCostAlone() {
    let check_duration = $(`.radiobtn input:checked`).attr('value');
    let check_frequency = $(`.checkbox__input:checked`).attr('value');
    // window.console.log(check_frequency)
    if (check_frequency === "QU") {
        $(`.radiobtn input[value="OM"]`).prop('disabled', true)
        $(`.radiobtn input[value="OM"]`).prop('checked', false)
    } else {
        $(`.radiobtn input[value="OM"]`).prop("disabled", false)
    }
    let price_div = $('.cartBuy__item-price').children();
    if (check_duration && check_frequency) {
        price_div.children('p').hide();
        price_div.children(`.${check_duration}.${check_frequency}`).show()
    }

}

function showCost() {
    $('.cartBuy__item-settings').each(function () {
        let classes = $(this).attr('class').split(/\s+/);
        let num = classes[1];
        let check_duration = $(`.${classes[0]}.${num} .radiobtn input:checked`).attr('value');
        let check_frequency = $(`.${classes[0]}.${num} .checkbox__input:checked`).attr('value');
        if (check_frequency === "QU") {
            $(`.${classes[0]}.${num} .radiobtn input[value="OM"]`).prop('disabled', true);
            $(`.${classes[0]}.${num} .radiobtn input[value="OM"]`).prop('checked', false);
        } else {
            $(`.${classes[0]}.${num} .radiobtn input[value="OM"]`).prop('disabled', false);
        }
        let price_div = $(this).siblings('.cartBuy__item-price').children();
        if (check_duration && check_frequency) {
            price_div.children('p').hide();
            price_div.children(`.${check_duration}.${check_frequency}`).show()
        }
    });
}

// $(document).ready(function(){
//     showCost()
// });

function cartBuy(a,b) {
    document.getElementById(a).style.display = "flex";
    document.getElementById(b).style.display = "none";
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
function changeButtonForm () {
    if ($('#callback-form-check').prop('checked', true)) {
        $('#callback-form-button').removeAttr('disabled')
    } else {
        $('#callback-form-button').attr('disabled', true)
    }

}

jQuery(function() {
    $(".search__input").on('keyup', function(){
        var value = $(this).val();
        $.ajax({
            url: "autocomplete",
            data: {
              'search': value
            },
            dataType: 'json',
            success: function (data) {
                list = data.list;
                $(".search__input").autocomplete({
                source: list,
                minLength: 3
                });
            }
        });
    });
  });
