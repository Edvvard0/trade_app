<div align="center">

# 🔄 TradeShop

**Веб-приложение на Django для размещения объявлений и обмена вещами между пользователями**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

</div>

---

## 📖 О проекте

TradeShop — доска объявлений с обменом: пользователь публикует объявление о вещи, находит чужие объявления через фильтры и полнотекстовый поиск и отправляет владельцу предложение обмена своей вещи на его. Получатель может принять или отклонить предложение.

<!-- TODO: скриншот -->

## ✨ Возможности

**Объявления**
- Создание, редактирование и удаление (только для авторизованных; правка и удаление — владельцем)
- Общий список с пагинацией и страница «Мои объявления»
- Фильтры по категории (машины, дома, хобби, другое) и состоянию (новый, б/у)
- Полнотекстовый поиск по заголовку и описанию (PostgreSQL `SearchVector` / `SearchRank`)

**Предложения обмена**
- Создание предложения: объявление-отправитель ↔ объявление-получатель + комментарий
- Списки «мои предложения» и «предложения, отправленные мне»
- Принять, отклонить, изменить и удалить предложение

**Аккаунты**
- Вход / выход и страница профиля на встроенной авторизации Django (страницы регистрации нет — пользователей создаёт админ через Django Admin)

## 🧱 Стек

| Технология | Роль |
|---|---|
| Python 3.12+ | Язык |
| Django 5.2 | Бэкенд, ORM, шаблоны, админка |
| Django Templates (HTML) | Фронтенд |
| PostgreSQL (`psycopg`) | БД и полнотекстовый поиск |
| Django `TestCase` | Тесты views |

## 🗂 Структура проекта

```text
trade_shop/
├── manage.py
├── trade_shop/     # settings, корневые urls, wsgi/asgi
├── ads/            # объявления: модели, формы, views, шаблоны, поиск (utils.py), тесты
├── exchange/       # предложения обмена: модели, формы, views, шаблоны, тесты
├── users/          # логин, логаут, профиль
└── core/           # базовый шаблон base.html
```

## 🚀 Быстрый старт

Нужны Python 3.12+ и запущенный PostgreSQL.

```bash
git clone https://github.com/Edvvard0/trade_app.git
cd trade_app

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# создайте БД trade_shop в PostgreSQL (параметры подключения — в settings.py)
cd trade_shop
python manage.py migrate
python manage.py createsuperuser # чтобы войти в приложение
python manage.py runserver
```

Приложение: http://127.0.0.1:8000

Тесты:

```bash
python manage.py test
```

## ⚙️ Конфигурация

Переменных окружения нет: параметры подключения к PostgreSQL заданы прямо в `trade_shop/trade_shop/settings.py` (секция `DATABASES`: БД `trade_shop`, `localhost:5432`). Перед деплоем вынесите в окружение `SECRET_KEY`, учётные данные БД и `DEBUG`.

## 🔌 Маршруты

| URL | Описание |
|---|---|
| `/` | Профиль (нужен вход) |
| `/login/`, `/logout/` | Вход и выход |
| `/ads/` | Список объявлений (`?category=`, `?condition=`, `?page=`) |
| `/ads/<id>/` | Страница объявления |
| `/ads/my_ads/` | Мои объявления |
| `/ads/create/`, `/ads/update/<id>/`, `/ads/delete/<id>/` | Управление объявлением |
| `/ads/search/` | Поиск |
| `/exchange/` | Мои предложения обмена |
| `/exchange/sent_me/` | Предложения, отправленные мне |
| `/exchange/create/` | Новое предложение |
| `/exchange/accept/<id>/`, `/exchange/reject/<id>/` | Принять / отклонить |
| `/exchange/update/<id>/`, `/exchange/delete/<id>/` | Изменить / удалить |
| `/admin/` | Django Admin |

<details>
<summary>📦 Модели</summary>

**Ad** — `user`, `title`, `description`, `image_url`, `category` (`cars` / `house` / `hobby` / `other`), `condition` (`new` / `used`), `created_at`.

**ExchangeProposal** — `ad_sender`, `ad_receiver`, `comment`, `status` (`pending` / `accepted` / `rejected`), `created_at`.

</details>

## 👤 Автор

**Эдвард Осипчук** · GitHub: [@Edvvard0](https://github.com/Edvvard0) · Telegram: [@Edward0076](https://t.me/Edward0076)
