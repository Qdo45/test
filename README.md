*Реализована апи /openfile*

*Структура*
 33.xml - Название файла ( Можно загружать свой )
 main.py - основной код 
 Unit_test - примеры тестов
 Dockerfile - файл для создания контейнера
 
 
*Параметры апи* 
Все параметры передаются чере form-data
file - файл, который будет обработан, обязательный параметр
person - True/False ( Разделение по сотрудникам, при True за каждый день будет видно кто сколько отработал) , по умолчанию False
start_date - дата начала проверки ( формат DD-MM-УУУУ) ( должны быть задана как дата старта, так и дата окончания) , по умолчанию будет браться и находиться из файла если оба не заданы
end_date - дата окончания проверки ( формат DD-MM-УУУУ) ( должны быть задана как дата старта, так и дата окончания) , по умолчанию будет браться и находиться из файла если оба не заданы


*Пример запроса:*
# wget doesn't support file upload via form data, use curl -F \
wget --no-check-certificate --quiet \
  --method GET \
  --timeout=0 \
  --header '' \
  --body-data 'person=False&start_date=01-01-2020&end_date=01-01-2020' \
   'http://127.0.0.1:5000/openfile'
   
 *Ошибки, которые возможны:*
  1 Нет обработки ошибок, когда даты кривые
  2 Если в один день работник приходил много раз и включена фильтрация по работникам, возможны дубли ( пока не исправлял) , для демо хватит
*Что предусмотрено*
  1 Защита, когда файл не передается или забывается параметр
  2 Защита от кривых path
  3 Защита от дата с> дата по 
  4 Параметры по умолчанию 
  5 Поиск начала и даты окончания, что-бы не было лишних дат
  6 
  
*Как запустить докер файл*
docker load -i image.tar
docker run -d -p 5000:5000 --name flask-app-test  my_flask_app
Теперь можно посылать запросы на http://127.0.0.1:5000/openfile
