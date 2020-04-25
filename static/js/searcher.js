var data = [];

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
            data = d.all_goods_names;
        },
        error: function(d) {
            console.log('error request to server');
        }
    });
});


function open_list(){
        if (searcher.value) {
            searcher.value = searcher.value[0].toUpperCase() + searcher.value.slice(1);
            let regV = RegExp.prototype.constructor(searcher.value);
            for(let i = 0; i < dropdown_menu_searcher.children.length; i++)
            {
                dropdown_menu_searcher.removeChild(dropdown_menu_searcher.firstChild)
            }
            for(let i = 0; i < data.length; i++)
            {
                if(data[i].match(regV)) {
                    element = document.createElement('a');
                    element.classList.add('dropdown-item');
                    element.type = 'button';
                    element.href = '/product/' + data[i];
                    element.textContent = data[i];
                    dropdown_menu_searcher.appendChild(element);
                }
            }
            $("#dropdownMenu").dropdown('show');
        }
        else {
            $("#dropdownMenu").dropdown('hide');
        }
        if(!dropdown_menu_searcher.children.length)
        {
            $("#dropdownMenu").dropdown('hide');
        }
    }
    searcher.addEventListener('input', () => open_list());