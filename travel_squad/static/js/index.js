function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function getCookie(name) {  // получаем csrf для отправли POST запроса 
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
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

function getURLParameter(sUrl, sParam) { 
    let sPageURL = sUrl.substring(sUrl.indexOf('?') + 1);
    let sURLVariables = sPageURL.split('&');
    for (let i = 0; i < sURLVariables.length; i++) {
        let sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}

function initPaginator() {
    document.body.querySelectorAll('.pagination > li > a')
            .forEach( link => link.addEventListener('click', pagination_link_clickHandler) );
}
function pagination_link_clickHandler(event){
    event.preventDefault(); // запрещаем событие 
    // из формы при нажатии на кнопки туда сюда через раз не удается получить url, из-з чего не происходит смены страницы   
    let path = event.target.href; // забираем путь 
    let page = getURLParameter(path, 'page');
    let csrftoken = getCookie('csrftoken');
    if (typeof page !== 'undefined') {
        jQuery.ajax({
            url: path, // по какому урлу 
            type: 'POST',
            data: {'page': getURLParameter(path, 'page'),
                    csrfmiddlewaretoken: csrftoken
                }, // забираем номер страницы, которую нужно отобразить и токен 

            beforeSend : function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success : function(json) {
                // Если запрос прошёл успешно и сайт вернул результат  
                if (json.result)
                {
                    window.history.pushState({route: path},'', path); // устанавливаем URL в строку браузера
                    jQuery("#articles").replaceWith(json.articles); // Заменяем div со списком статей на новый
                    initPaginator(); // Переинициализируем пагинатор
                }
            }
        });
    }
}
initPaginator();