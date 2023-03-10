# stripe_django_test_case

Payment integration using Stripe (testing mode) and Django.

В проекте реализована имитация совершения платежей с ипользованием системы Stripe (Stripe Payment Intent):

   - Запуск проекта в контейнерах Docker;
   - Использовал переменные среды;
   - В Django четыре модели для тестовой работы с платежами: Order, Items, Discount и Tax;
   - Пользовательский шаблон страницы оплаты заказа методом Payment Intent.


Рекомендации по установке и настройке проекта:

1) В файле ".env.sample" изменить данные для тестового публичного и секретного API ключа из личного кабинета сайта Stripe. Далее, переименовать файл в ".env"

2) Для запуска приложения в контейнерах исполнить в терминале следующие команды:
    
    - docker-compose build
    
    - docker-compose run --rm app sh -c "python manage.py createsuperuser"        # ввести данные для создания суперпользователя

3) После этого можно открыть страницу панели администратора http://127.0.0.1:8000/admin и добавить несколько записей для поля Items (товары сайта), пару записей поля Discounts (скидки в виде дисконта) и можно добавить запись в поле Tax (комиссия).

4) Перейти на главную страницу сайта и выбрать несколько "товаров" для добавления в заказ. Выбрать скидку и нажать кнопку оплатить (Pay).

5) Ввести номер карты 4242 4242 4242 4242 и в остальных полях любые валидные данные. Такой номер карты используется в целях тестирования на сайте системы платежей через Stripe. В случае если платеж успешно исполнится в окне будет выведено сообщение.

Ниже пример работы приложения:

![alt text](https://github.com/likeprogrsv/stripe_django_test_task/blob/main/example.gif)