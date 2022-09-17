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
        listItem.innerHTML = "<span>" + item + "</span> <button onclick='unselect(this)'>x</button>";

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

function init() {
    var base = [43.3293017383, 36.6570520132],
        base_zone37 = {x: 310050, y: 4800050};
    var list = [{id: 1, x: 334500, y: 5006900}, {id: 2, x: 392100, y: 5005900}] // здесь будут данные обо всех виноградниках из БД
    var myMap = new ymaps.Map("map", {
        center: base,
        zoom: 5
    });

    for (i = 0; i < list.length; i++) {
        var right_distance = list[i].x - base_zone37.x,
            up_distance = list[i].y - base_zone37.y;
        var go_right = ymaps.coordSystem.geo.solveDirectProblem(
            base,
            [0, 1],
            right_distance
        ).endPoint;

        var go_up = ymaps.coordSystem.geo.solveDirectProblem(
            go_right,
            [1, 0],
            up_distance
        ).endPoint;


        var placemark = new ymaps.Placemark(
            go_up,
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

