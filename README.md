#   Курсовая работа
_________________________________________________
## Веб-сервисы
### Главная
#### В JSON-файл выводятся данные в формате:
Приветствие в формате — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» - в зависимости от текущего времени. 

По каждой карте: 
* последние 4 цифры карты;
* общая сумма расходов;
* кешбэк (1 рубль на каждые 100 рублей).

Топ-5 транзакций по сумме платежа.

Курс валют.

Стоимость акций из S&P500.
## Сервисы
### Выгодные категории повышенного кешбэка
Сервис позволяет проанализировать, какие категории были наиболее выгодными для выбора в качестве категорий повышенного кешбэка. A точнее JSON-afqk с анализом, сколько на каждой категории можно заработать кешбэка
## Отсчеты
### Траты по категории
Функция возвращает траты по заданной категории.


## VIEWS информацмя 

### `main_viewers(time_range: str)`
Описание

Функция main_viewers является основной функцией для анализа данных и формирования отчета. Она выполняет следующие задачи:

Чтение данных из xls файла.

Запись данных в JSON файл.

Чтение данных из JSON файла.

Фильтрация транзакций по указанному диапазону дат.

Получение приветственного сообщения в зависимости от текущего времени.

Получение информации о картах, их тратах и кэшбэках.

Определение топ-5 самых дорогих транзакций.

Получение текущих курсов валют.

Получение текущих цен акций.

Формирование итогового отчета и запись его в JSON файл.

Аргументы
time_range (str): Строка, определяющая диапазон дат для фильтрации транзакций в формате "YYYY-MM-DD HH:MM
".

Возвращает

Dict[str, Any]: Словарь, содержащий сформированный отчет с данными о приветствии, картах, топ-5 транзакциях, курсах валют и ценах акций.

В основной части кода происходит чтение данных о транзакциях, вычисление общей суммы расходов, обработка данных о картах, выборка самых дорогих транзакций, получение курсов валют и цен на акции, а затем сохранение всех данных в формате JSON в файл "operations_data.json".

тесты есть

## reports информация

### `spending_by_category(df: pd.DataFrame, category: str, date: str = None)`
### Описание
Функция spending_by_category рассчитывает общую сумму расходов по заданной категории за последние три месяца от указанной даты. Если дата не указана, используется текущая дата.

### Аргументы
df (pd.DataFrame): DataFrame с данными о транзакциях.

category (str): Категория транзакций, по которой необходимо рассчитать расходы.
date (str, optional): Дата, от которой отсчитываются три месяца. Формат: "dd-mm-yyyy".

Если не указана, используется текущая дата.
Возвращает

Dict[str, Any]: Словарь, содержащий категорию и общую сумму расходов по ней за последние три месяца.
### Описание работы функции
Проверка даты: Если дата не указана, используется текущая дата. В противном случае, дата преобразуется из строки в объект datetime.

Вычисление конечной даты: Определяется дата три месяца назад от указанной даты.
Фильтрация данных: Фильтруются транзакции, соответствующие указанной категории и попадающие в заданный диапазон дат.

Суммирование расходов: Рассчитывается общая сумма расходов по фильтрованным транзакциям.
Формирование результата: Возвращается словарь с категорией и общей суммой расходов.

### Декоратор `save_report_to_file`

## `cashback_count(data: Any, year: int, month: int)`

Функция `spending_by_category` украшена декоратором `save_report_to_file`, который сохраняет результат функции в JSON файл. Декоратор выполняет следующие задачи:

Определение имени файла: Если имя файла не указано при вызове декоратора, используется "report.json" по умолчанию.

Сохранение данных: Результат функции сохраняется в JSON файл с указанным именем.
Логирование: В файл логов записывается сообщение об успешном сохранении данных.
Пример использования декоратора:

# services  информация
## Описание
Функция `cashback_count` анализирует данные транзакций и вычисляет, сколько кэшбэка можно заработать по каждой категории в указанном месяце года. Результаты сохраняются в JSON файл.

## Аргументы
`data (Any)`: Список транзакций в виде словарей, где каждая транзакция содержит ключи, такие как "Дата операции", "Категория" и "Кэшбэк".

`year (int)`: Год, за который нужно проанализировать кэшбэк.

`month (int)`: Месяц, за который нужно проанализировать кэшбэк.

## Возвращает

`None`: Функция не возвращает значение, но сохраняет результаты анализа в JSON файл.

## Описание работы функции

Проверка данных: Если данные транзакций отсутствуют, функция записывает ошибку в лог и завершает работу.

Инициализация счетчика: Создается объект Counter для подсчета кэшбэка по категориям.

Анализ транзакций: Проход по каждой транзакции:

Преобразование строки с датой операции в объект datetime.

Проверка соответствия года и месяца операции указанным значениям.

Если операция соответствует, добавление кэшбэка к соответствующей категории.

Сохранение результатов: Результаты анализа сохраняются в JSON файл:

Если файл не найден, записывается ошибка в лог.

Если сохранение прошло успешно, записывается сообщение об успешной записи.


# utils информация 
`setup_logging(name_file: str)`

Настраивает логирование и возвращает объект логгера.
name_file: имя файла для логов.
`read_xls(file_name: Any)` 

Читает данные из xls файла и возвращает их в виде списка словарей.
file_name: имя файла xls.

`write_in_json(dict_pd: List[Dict[str, Any]]) `

Записывает данные в JSON файл.
dict_pd: данные в виде списка словарей.

`read_in_json()`

Читает данные из JSON файла и возвращает их.

`read_user_settings_currency()`

Читает пользовательские настройки для валют из файла user_settings.json.

`read_user_settings_stocks()`

Читает пользовательские настройки для акций из файла user_settings.json.

`filter_transactions_date(transactions: List[Dict[str, Any]], date_str: str) `

Фильтрует транзакции по указанной дате в виде диапазона.
transactions: список транзакций.
date_str: строка даты в формате "YYYY-MM-DD HH:MM
".

`receive_greeting()`

Возвращает приветствие в зависимости от текущего времени.

`info_cards(data_transactions: List[Dict[str, Any]])` 

Возвращает информацию о картах и их транзакциях.
data_transactions: список транзакций.

`geting_csrds(transactions: Any)` 

Возвращает список с информацией о картах, тратах и кэшбэках.
transactions: список транзакций.

`top_5_transactions(data: List[Dict[str, Any]])`

Возвращает список из пяти самых дорогих транзакций.
data: список транзакций.

`api_currency(currency: List[str])`

Возвращает текущий курс валют.
currency: список валют.

`api_stock(stocks: Any)`

Возвращает текущую цену акций.
stocks: список акций.


