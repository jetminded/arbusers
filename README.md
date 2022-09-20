# AgroCodeHack - Задача №3
## Перспективные земли для виноградников

Создание сервиса по поиску перспективных земель для выращивания винограда в Краснодарском крае.

### Условие задачи:

Правильный выбор земельного участка для посадок винограда позволяет производить качественное вино, которое отражает характеристики территории. На хорошем участке можно также сэкономить на внесении удобрений, пестицидов и других видах коррекции плодородия.
Выбор участка определяет всю дальнейшую производственную цепочку: выбор сортов подвоев и привоев, их размещение на участке, непосредственно проектные решения. Это первый и один из самых важных этапов проектирования виноградника.


Под перспективными для виноградарства землями подразумеваются территории, которые:

- заняты естественными растительными сообществами или используются для возделывания иных сельскохозяйственных культур (не винограда)
- имеют природные характеристики, схожие с одной или несколькими существующими территориями виноградарских хозяйств

Необходимо найти перспективные для возделывания винограда земли в Краснодарском крае.

#### Что дано?

- Данные о существующих виноградных хозяйствах Краснодарского края.
- Массивы климатической, геоморфологической и другой информации по Краснодарскому краю разрешением 20—200 м/пиксель.

#### Результат 

Сервис поиска перспективных земель, в котором пользователь выбирает одно или несколько существующих виноградных хозяйств, а на карте Краснодарского края выделяются области с территориями, близкими по природным характеристикам. На меру «близости» выделенных территорий пользователь может влиять выбором допустимого разброса анализируемых природных характеристик.

## О нашем решении

Решение доступно по ссылке [arbusers.ru](http://arbusers.ru).

#### Идея алгоритма подбора земель:

Из постановки задачи и экспертных знаний мы можем считать, что данные удовлетворяют гипотезе непрерывности, т.е. мы можем считать что в среднем на близко расположенных землях схожие природные условия. Поэтому анализ подходящих земель для виноградников реализован с использованием метрики схожести. 

TODO

#### Для сборки проекта в дебаге:

- Проверьте наличие пакетов, в противном случае установите их:
    - ```sudo apt install python3-pip```
    - ```sudo apt-get install python3-venv```

- При скачивании этого репозитория в настройках флаг дебага истинен, но вы можете проверить это вручную:
    - Откройте файл ```settings.py```, который лежит в ```source/vineyards/vineyards```
    - Проверьте, что параменной DEBUG присвоено значение True: ```DEBUG = True```

- Создайте виртуальное окружение в корне проекта: ```python3 -m venv .venv```

- Активируйте его: ```source .venv/bin/activate```

- После этого подгрузите все необходимые зависимости: ```pip3 install -r requirements.txt```

- Далее перейдите в приложение vineyards: ```cd source/vineyards/```

- Загрузите статику и накатите все необходимые миграции:
    - ```python3 manage.py collectstatic``` 
    - ```python3 manage.py makemigrations```
    - ```python3 manage.py migrate```
    
- Далее необходимо наполнить базу данных с помощью скрипта: ```cd .. && python3 parse_vineyards.py```

- Для запуска на 8080 порту выполните: ```cd vineyards && python3 manage.py runserver 8080```

*Проект создали Спицын Николай, Феоктистов Дмитрий, Чубенко Полина, Савичев Дмитрий, Сбродов Егор*
