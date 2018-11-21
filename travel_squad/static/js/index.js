function getURLParameter(sUrl, sParam) { 
    console.log(sUrl.length);
    let pageParameterPos = 0;
    for (let i = sUrl.length - 1; i >= 0; i--) {
        console.log(sUrl[i]);
        if (sUrl[i] == '?') {
            pageParameterPos = i;
            break;
        }
    }
    let sPageURL = sUrl.substring(pageParameterPos + 1);
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

function initTags() {
    // getElementsByClassName возвращает не array с которым может работать forEach
    Array.from(document.body.getElementsByClassName('tag'))
        .forEach(link => link.addEventListener('click', tag_link_clickHandler ));
}

function initSearchButton() {
    document.getElementById('search').addEventListener('click', search_clickHandler);
}


function search_clickHandler(event){
    event.preventDefault(); // запрещаем событие 
    let form = document.getElementById('search_form')
    let input = document.getElementById('inputed_query')
    let path = form.action + '?' + input.name + '=' + input.value;
    console.log('path: ', path);
    console.log('query: ', input.value);

    if (typeof input.value !== 'undefined') {
        jQuery.ajax({
            url: path, // по какому урлу 
            type: 'GET',
            success : function(json) {
                // Если запрос прошёл успешно и сайт вернул результат  
                if (json.result)
                {
                    console.log(json.articles);
                    window.history.pushState({route: path},'', path); // устанавливаем URL в строку браузера
                    jQuery("#articles").replaceWith(json.articles); // Заменяем div со списком статей на новый
                    initPaginator(); // Переинициализируем пагинатор
                }
            }
        });
    }
}

function tag_link_clickHandler(event){
    event.preventDefault(); // запрещаем событие 
    let path = event.target.href; // забираем путь 
    let tag = event.target.textContent // берем tag из html кода в виде текста 

    if (typeof tag !== 'undefined') {
        jQuery.ajax({
            url: path, // по какому урлу 
            type: 'GET',
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


function pagination_link_clickHandler(event){
    event.preventDefault(); // запрещаем событие 
    // из формы при нажатии на кнопки туда сюда через раз не удается получить url, из-з чего не происходит смены страницы   
    let path = event.target.href; // забираем путь 
    console.log('pagination path: ', path);
    let page = getURLParameter(path, 'page');
    console.log('pagination page: ', page);
    if (typeof page !== 'undefined') {
        jQuery.ajax({
            url: path, // по какому урлу 
            type: 'GET',
            // data: {'page': page }, 
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
initTags();
initSearchButton();
