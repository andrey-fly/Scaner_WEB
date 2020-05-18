var goods_data = [];
var categories_data = [];

var numbers_is_animated = false;

function animate_numbers()
{
    if(window.pageYOffset > animated_numbers.offsetHeight){
      $('#num').animate({
            num: goods_data.length - 1
        }, {
            duration: 3000,
            step: function(num) {
                this.innerHTML = (num + 1).toFixed(0)
            }
        });
        $('#num2').animate({
            num: amount_of_users - 1 /* - начало */
        }, {
            duration: 2000,
            step: function(num) {
                this.innerHTML = (num + 1).toFixed(0)
            }
        });
        $('#num3').animate({
            num: amount_of_picture - 3 /* - начало */
        }, {
            duration: 5000,
            step: function(num) {
                this.innerHTML = (num + 3).toFixed(0)
            }
        });
        numbers_is_animated = true;
  }
}

function open_list(){
    let len = dropdown_menu_searcher.children.length;
    for(let i = 0; i < len; i++)
    {
        dropdown_menu_searcher.removeChild(dropdown_menu_searcher.firstChild);
    }

    if (searcher.value) {
        searcher.value = searcher.value[0].toUpperCase() + searcher.value.slice(1);
        let regV = RegExp.prototype.constructor(searcher.value);

        for(let i = 0; i < goods_data.length; i++)
        {
            if(goods_data[i].match(regV)) {
                element = document.createElement('a');
                element.classList.add('dropdown-item');
//                element.type = 'button';
                element.href = '/product/' + goods_data[i] + '/';
                element.textContent = goods_data[i];
                dropdown_menu_searcher.appendChild(element);
            }
        }

        for(let i = 0; i < categories_data.length; i++)
        {
            if(categories_data[i][0].match(regV)) {
                element = document.createElement('a');
                element.classList.add('dropdown-item');
//                element.type = 'button';
                element.href = '/category/' + categories_data[i][1];
                element.textContent = categories_data[i][0];
                dropdown_menu_searcher.appendChild(element);
            }
        }

        $("#dropdown_menu_searcher").dropdown('show');
    }
    else {
        $("#dropdown_menu_searcher").dropdown('hide');
    }
    if(!dropdown_menu_searcher.children.length)
    {
        $("#dropdown_menu_searcher").dropdown('hide');
    }
}

$(document).ready(function() {
    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        url: '/',
        method: 'POST',
        data: {'action': 'initial_searcher'},
        success: function(d) {
            console.log(d);
            goods_data = d.all_goods_names;
            categories_data = d.all_categories;
            amount_of_picture = d.amount_of_pictures;
            amount_of_users = d.amount_of_users;
            animate_numbers();
        },
        error: function(d) {
            console.log('error request to server');
        }
    });

    searcher.addEventListener('input', () => open_list());

    window.addEventListener('scroll', function() {
        if(!numbers_is_animated)
            animate_numbers();
    });

});