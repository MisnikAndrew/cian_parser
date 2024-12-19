# Телеграм бот для скоринга квартир с сайта ЦИАН

Телеграм бот взаимодействует с API сайта cian.ru, получает информацию о квартирах по фильтрам и самостоятельно оценивает "крутость" квартир. <br>
В результате собирает отчет с информацией о квартирах и выдает пользователю в текстовом и табличном формате. <br>

# Параметры скоринга
1. Цена квартиры за месяц <br>
2. Близость к метро совокупно с "крутостью" станции метро (крутость станции метро определяется с использованием https://github.com/MisnikAndrew/metro_scoring ) <br>
3. Количество месяцев предоплаты, размер депозита и комиссии <br>
4. Площадь квартиры - общая, жилая, площадь кухни <br>
5. Количество комнат <br>
6. Количество лождий/балконов <br>
7. Количество раздельных/совмещенных С/У <br>
8. Наличие посудомойки / кондиционера <br>
9. Тип ремонта / направление куда выходят окна <br>
10. Возможность заселения с детьми / с животными <br>



# Запуск в докере
1. Клонировать репозиторий https://github.com/MisnikAndrew/cian_parser.git <br>
2. Запустить ./run_docker.sh <br>
4. Зайти в диалог с @CianParsingScoringBot <br>
5. Ввести команду /start и заполнить нужные значения. <br>


# Описание файлов
debug_data - папка с примерами отчетов и с ноутбуками, в которых можно запускать это без использования telegram-бота <br>
src - исходный код бота; src/telegram_bot.py - запускаемый файл <br>
src/utils - утилиты для скоринга и построения отчета о квартирах  <br>
Dockerfile - файл для создания докер-образа <br>
run_docker.sh - скрипт для запуска Docker-файла <br>
requirements.txt - обязательные библиотеки для запуска <br>


