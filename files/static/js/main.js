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

function showCost(a, b, c, d, i) {
    if  ($(`.${i}` + 'QU').prop("checked") || $(`.${i}` + 'MU').prop("checked")) {
        $(`.${i}M`).hide()
        $(`.${i}Q`).hide()
        if ($(`.${i}` + 'MU').prop("checked")) {
            $(`.${a}.${i}M`).show()
            $(`.${b}.${i}M`).hide()
            $(`.${c}.${i}M`).hide()
            $(`.${d}.${i}M`).hide()
        } else {
            $(`.${a}.${i}Q`).show()
            $(`.${b}.${i}Q`).hide()
            $(`.${c}.${i}Q`).hide()
            $(`.${d}.${i}Q`).hide()
        }
    }
}

function changeFrequency(a) {
    $(`.${a}` + 'D').prop('checked', false);
    $(`.${a}M`).hide()
    $(`.${a}Q`).hide()

}
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
