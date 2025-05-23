# TradeShop

TradeShop — это веб-приложение на базе Django для размещения и обмена
товарами. Пользователи могут создавать объявления, просматривать чужие объявления,
выполнять поиск, фильтровать по категориям и состоянию,
а также отправлять предложения обмена.
Приложение включает авторизацию, пагинацию и тестирование.

---

## Основные возможности

### Объявления:
- Создание, редактирование, удаление объявлений (только для владельцев).
- Просмотр всех объявлений или только своих.
- Фильтрация по категориям (машины, дома, хобби, другое) и состоянию (новый, б/у).
- Поиск по заголовку и описанию.

### Предложения обмена:
- Отправка предложений обмена между объявлениями.
- Просмотр списка предложений с фильтрацией по статусу (ожидает, принята, отклонена).


### Безопасность:
- Аутентификация через Django для создания, редактирования и удаления.
- Проверка прав доступа (только владелец может редактировать/удалять).

---

## Технологии

- Backend: Django 4.x  
- Frontend: HTML, CSS, Django templates  
- База данных:  PostgreSQL
- Тестирование: Django TestCase  
- Python: 3.8+

---

## Установка


### Шаги

1. Клонируйте репозиторий:  
   ```bash
   git clone https://github.com/Edvvard0/trade_app.git
   cd TradeShop
Создайте и активируйте виртуальное окружение:

```bash
Копировать
Редактировать
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

```
```commandline
pip install -r requirements.txt
```

```commandline
python manage.py makemigrations
python manage.py migrate
```


```commandline
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000

Структура проекта
```bash
Копировать
Редактировать
TradeShop/
├── ads/
│   ├── migrations/
│   ├── templates/ads/
│   │   ├── all_ads.html            # Список объявлений
│   │   ├── current_ad.html         # Страница конкретного объявления
│   │   ├── create_ads.html         # Форма создания объявления
│   │   ├── update_ad.html          # Форма редактирования объявления
│   │   ├── exchange_proposals.html# Список предложений обмена
│   ├── templatetags/
│   │   ├── ad_filters.py           # Кастомные фильтры Django
│   ├── __init__.py
│   ├── admin.py                    # Настройки админ-панели
│   ├── apps.py
│   ├── forms.py                    # Формы для создания/редактирования объявлений
│   ├── models.py                   # Модели (Ad, ExchangeProposal)
│   ├── tests.py                    # Тесты для views
│   ├── urls.py                     # Маршруты приложения
│   ├── utils.py                    # Утилиты (q_search)
│   ├── views.py                    # Представления
├── core/
│   ├── templates/core/
│   │   ├── base.html               # Базовый шаблон
├── trade_shop/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Настройки проекта
│   ├── urls.py                     # Главные маршруты
│   ├── wsgi.py
├── manage.py
├── requirements.txt
├── README.md

```

Основные маршруты
/ — Список всех объявлений (all_ads)

/current_ad/<id>/ — Просмотр конкретного объявления

/my_ads/ — Список объявлений текущего пользователя

/create/ — Создание нового объявления (требуется авторизация)

/update/<id>/ — Редактирование объявления (только для владельца)

/delete/<id>/ — Удаление объявления (только для владельца)

/search/ — Поиск объявлений по запросу

/exchange_proposals/ — Список предложений обмена (требуется авторизация)

# Модели
### Ad
user: Владелец (ForeignKey на User)

title: Заголовок (CharField)

description: Описание (TextField)

category: Категория (CharField, ключи из CATEGORY_CHOICES)

condition: Состояние (CharField, ключи из CONDITION_CHOICES)

image_url: URL изображения (URLField, опционально)

created_at: Дата создания (DateTimeField)

### ExchangeProposal
ad_sender: Объявление отправителя (ForeignKey на Ad)

ad_receiver: Объявление получателя (ForeignKey на Ad)

comment: Комментарий (CharField)

status: Статус (CharField, ключи из STATUS_CHOICES)

created_at: Дата создания (DateTimeField)


