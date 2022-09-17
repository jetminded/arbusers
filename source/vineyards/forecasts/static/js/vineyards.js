var list;
var selected_vineyards = new Set();
ymaps.ready(init);
function unselect(item) {
    let text = item.parentElement.getElementsByTagName("span")[0].innerText;
    console.log([text]);
    console.log(selected_vineyards.has(text));
    console.log(selected_vineyards);
    selected_vineyards.delete(text);
    console.log(selected_vineyards.has(text));
    item.parentElement.remove();
}

function make_list(list) {
    let listContainer = document.getElementById("selected_vineyards"),

        // Make the list
        listElement = document.getElementById("selected_vineyards_list"),

        // Set up a loop that goes through the items in listItems one at a time
        numberOfListItems = list.size,
        listItem,
        i;

    // Add it to the page

    listContainer.appendChild(listElement);
    console.log(numberOfListItems);
    const iterator = list[Symbol.iterator]();
    for (i = 0; i < numberOfListItems; ++i) {
        // Create an item for each one
        listItem = document.createElement('li');

        // Add the item text
        let item = iterator.next().value;
        console.log(item);
        listItem.innerHTML = "<span>" + item + '</span> <a role="button" tabindex="0"  onclick="unselect(this)" class="cross-btn">&#10799;</a> ';

        // Add listItem to the listElement
        listElement.appendChild(listItem);
    }
}

function placemark_event(e) {
    var vineyard = e.get("target").properties.get("iconContent");
    if (selected_vineyards.has(vineyard)) {
        selected_vineyards.delete(vineyard)
    } else {
        selected_vineyards.add(vineyard)
    }
    console.log(selected_vineyards);
    let list = document.getElementById("selected_vineyards_list");
    list.innerHTML = '';
    make_list(selected_vineyards);
}

$.ajax({
    url: "get_database",
    type: "GET",
    dataType: "json",
    data: {},
    success: function(result){
        console.log(result);
        var json = result;

        if (!result['success']) {
            // сообщение об ошибке
            alert("wow");
        }
        else {
            // сообщение об успехе
            list = json.data;
        }
    }
});

function init() {
    var base = [45.1969786974, 39.1890641332];
    var myMap = new ymaps.Map("map", {
        center: base,
        zoom: 8
    });

    for (i = 0; i < list.length; i++) {
        console.log(list[i]);
        var placemark = new ymaps.Placemark(
            [list[i].x, list[i].y],
            {
                balloonContent: '',
                iconContent: list[i].id.toString()
            },
            {
                preset: "islands#yellowStretchyIcon",
                // Отключаем кнопку закрытия балуна.
                balloonCloseButton: false,
                // Балун будем открывать и закрывать кликом по иконке метки.
                hideIconOnBalloonOpen: false
            }
        );

        placemark.events.add('click', placemark_event);

        myMap.geoObjects.add(placemark);
    }
}

