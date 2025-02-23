# Вариант 22
Разработать инструмент командной строки для визуализации графа 
зависимостей, включая транзитивные зависимости. Сторонние средства для 
получения зависимостей использовать нельзя. 
Зависимости определяются по имени пакета языка Java (Maven). Для 
описания графа зависимостей используется представление Graphviz. 
Визуализатор должен выводить результат в виде сообщения об успешном 
выполнении и сохранять граф в файле формата png. 

python3 graph.py -v /opt/homebrew/bin/dot -p org.apache.commons:commons-lang3 -o graph.png -r /Users/<имя_пользователя>/.m2/repository
Аргументы команды:

python3 graph.py — запуск скрипта graph.py на Python.
-v /opt/homebrew/bin/dot — путь к программе для визуализации графов. В данном случае используется Graphviz, установленный через Homebrew (менеджер пакетов для macOS). Программа dot отвечает за рендеринг графов в формате PNG.
-p org.apache.commons:commons-lang3 — пакет Maven, для которого строится граф зависимостей. Формат: groupId:artifactId.
-o graph.png — путь к выходному файлу (изображению графа в формате PNG).
-r /Users/<имя_пользователя>/.m2/repository — путь к локальному Maven-репозиторию, в котором находятся загруженные артефакты и их POM-файлы.


Как найти эквиваленты для Windows
1. Установите Python

Убедитесь, что Python установлен. Если его нет, скачайте Python для Windows.

2. Установите Graphviz

Скачайте Graphviz для Windows с официального сайта: Graphviz Download.
Установите Graphviz и добавьте путь к dot.exe в системную переменную PATH. Обычно Graphviz устанавливается в папку:
C:\Program Files\Graphviz\bin.

3. Путь к Maven-репозиторию

Maven хранит загруженные артефакты и их POM-файлы в папке:
C:\Users\<Ваш_пользователь>\.m2\repository.
Этот путь нужно указать вместо /Users/vardges/.m2/repository.

5. Путь к dot.exe

Убедитесь, что dot.exe корректно установлен и его путь добавлен в PATH. Проверьте, работает ли команда:
dot -V
Если Graphviz установлен, вы увидите версию программы.

6. Проверка Maven-репозитория

Убедитесь, что локальный репозиторий Maven содержит необходимый артефакт org.apache.commons:commons-lang3. Для этого проверьте наличие POM-файла:
C:\Users\<Ваш_пользователь>\.m2\repository\org\apache\commons\commons-lang3\3.12.0\commons-lang3-3.12.0.pom
Если POM-файл отсутствует, загрузите его:
mvn dependency:get -Dartifact=org.apache.commons:commons-lang3:3.12.0

7. Запуск скрипта

Выполните команду:

python graph.py -v "C:\Program Files\Graphviz\bin\dot.exe" -p org.apache.commons:commons-lang3 -o graph.png -r "C:\Users\<Ваш_пользователь>\.m2\repository"

Скрипт создаст файл graph.png в текущей рабочей директории. Он будет содержать граф зависимостей для пакета org.apache.commons:commons-lang3.

8. Запуск тестов

python3 -m unittest test_graph.py - запуск тестов
