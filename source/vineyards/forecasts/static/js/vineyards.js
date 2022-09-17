var list;
var selected_vineyards = {};
ymaps.ready(init);
function unselect(item) {
    let text = item.parentElement.getAttribute('id');
    console.log('text' + text);
    delete selected_vineyards[text];
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

    for (const [key, value] of Object.entries(list)) {
        // Create an item for each one
        listItem = document.createElement('li');
        listItem.setAttribute("id", key);

        // Add the item text
        listItem.innerHTML = "<span>(" + key + ') ' + value + '</span> <a role="button" tabindex="0"  onclick="unselect(this)" class="cross-btn">&#10799;</a> ';

        // Add listItem to the listElement
        listElement.appendChild(listItem);
    }
}

function placemark_event(e) {
    var vineyard = e.get("target").properties.get("iconContent");
    var vineyard_name = e.get("target").properties.get("hintContent");
    console.log(vineyard + vineyard_name);
    if (vineyard in selected_vineyards) {
        delete selected_vineyards[vineyard]
    } else {
        selected_vineyards[vineyard] = vineyard_name;
    }

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
        var placemark = new ymaps.Placemark(
            [list[i].x, list[i].y],
            {
                iconContent: list[i].id.toString(),
                hintContent: list[i].name
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

    document.getElementById("submit_btn").onclick = function() {
        document.getElementById("chosen_vineyards").value = JSON.stringify(selected_vineyards);
    }
}

