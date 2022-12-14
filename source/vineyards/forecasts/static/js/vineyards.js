var list;
var wineries;
var placemarks = [];
var wineries_placemarks = [];
ymaps.ready(init);
function unselect(item) {
    let text = item.parentElement.getAttribute('id');
    placemarks[parseInt(text) - 1].options.set("preset", "islands#yellowStretchyIcon");
    delete selected_vineyards[text];
    item.parentElement.remove();
}

function make_list(list) {
    let listContainer = document.getElementById("selected_vineyards"),

        // Make the list
        listElement = document.getElementById("selected_vineyards_list"),

        // Set up a loop that goes through the items in listItems one at a time
        listItem;

    // Add it to the page

//    listContainer.appendChild(listElement);
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
    if (vineyard in selected_vineyards) {
        e.get("target").options.set("preset", "islands#yellowStretchyIcon");
        delete selected_vineyards[vineyard]
    } else {
        e.get("target").options.set("preset", "islands#redStretchyIcon");
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

$.ajax({
    url: "get_database_winery",
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
            wineries = json.data;
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
        placemarks[i] = new ymaps.Placemark(
            [list[i].x, list[i].y],
            {
                iconContent: list[i].id.toString(),
                hintContent: list[i].name
            },
            {
                preset: ((i + 1 in selected_vineyards) ? "islands#redStretchyIcon" : "islands#yellowStretchyIcon"),
                visible: true,
                // Отключаем кнопку закрытия балуна.
                balloonCloseButton: false,
                // Балун будем открывать и закрывать кликом по иконке метки.
                hideIconOnBalloonOpen: false
            }
        );

        placemarks[i].events.add('click', placemark_event);

        myMap.geoObjects.add(placemarks[i]);
    }

    for (i = 0; i < wineries.length; i++) {
        wineries_placemarks[i] = new ymaps.Placemark(
            [wineries[i].x, wineries[i].y],
            {
                iconContent: wineries[i].id.toString(),
                hintContent: wineries[i].name
            },
            {
                preset: "islands#greenStretchyIcon",
                visible: true,
                // Отключаем кнопку закрытия балуна.
                balloonCloseButton: false,
                // Балун будем открывать и закрывать кликом по иконке метки.
                hideIconOnBalloonOpen: false
            }
        );

        myMap.geoObjects.add(wineries_placemarks[i]);
    }

    make_list(selected_vineyards);

    for (i = 0; i < result["center"].length; i++) {
        console.log("lol");
        var myRectangle = new ymaps.Rectangle([
           result["left"][i],
           result["right"][i]
        ]);

        var result_placemark = new ymaps.Placemark(
            result["center"][i],
            {
                iconContent: (i+1).toString(),
            },
            {
                preset: "islands#blueStretchyIcon",
                visible: true,
                // Отключаем кнопку закрытия балуна.
                balloonCloseButton: false,
                // Балун будем открывать и закрывать кликом по иконке метки.
                hideIconOnBalloonOpen: false
            }
        );

        myMap.geoObjects.add(myRectangle);
        myMap.geoObjects.add(result_placemark);
    }

    document.getElementById("submit_btn").onclick = function() {
        document.getElementById("chosen_vineyards").value = JSON.stringify(selected_vineyards);
    }
}

function filter(item) {
    var grape = item.parentElement.getElementsByTagName("p")[0].innerText;
    for (i = 0; i < list.length; i++) {
        var visible = placemarks[i].options.get("visible");
        if (list[i].grape == grape && visible != item.checked) {
            placemarks[i].options.set("visible", !visible);
        }
    }
}

function filter_wineries(item) {
    for (i = 0; i < wineries.length; i++) {
        var visible = wineries_placemarks[i].options.get("visible");
        if (visible !== item.checked) {
            wineries_placemarks[i].options.set("visible", !visible);
        }
    }
}

