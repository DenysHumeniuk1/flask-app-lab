# Лабораторна робота №8 — ORM. Зв'язки

Робота продовжує Flask-проєкт попередньої лабораторної. Реалізовано зв'язок User–Post (one-to-many), Post–Tag (many-to-many), вибір автора і кількох тегів у формі, відображення тегів та приклади оптимізації завантаження.

## 1. Підготовка середовища

Активуйте віртуальне середовище та встановіть залежності:

```bash
pip install -r requirements.txt
```

Переконайтеся, що `.env` налаштований за потреби. У цьому проєкті SQLite використовується за замовчуванням.

## 2. Міграція

У корені проєкту:

```bash
flask db upgrade
```

Нова міграція `a10000000006_add_users_tags_relationships.py` створює таблиці `users`, `tags`, `post_tags`, додає `posts.user_id` і переносить попередні значення `author` у таблицю користувачів. Попередні міграції не видаляються.

## 3. Додати двох користувачів і призначити авторів (пункти 5–7)

Запустіть:

```bash
flask shell
```

Виконайте команди:

```python
from app.extensions import db
from app.posts.models import User, Post

user1 = User(username="user1", email="user1@example.com", password="123456")
user2 = User(username="user2", email="user2@example.com", password="123456")
db.session.add_all([user1, user2])
db.session.commit()

posts = db.session.scalars(db.select(Post).order_by(Post.id)).all()
for post in posts:
    post.user = user2
for post in posts[:1]:
    post.user = user1
db.session.commit()

user2_posts = db.session.scalars(db.select(Post).where(Post.user_id == 2)).all()
user1_posts = db.session.scalars(db.select(Post).where(Post.user_id == 1)).all()
print("Пости user2:", user2_posts)
print("Пости user1:", user1_posts)
```

Якщо міграція вже перенесла старих авторів, у таблиці `users` можуть існувати користувачі до додавання цих двох. Для пунктів із `id=1` та `id=2` перевірте фактичні ID через `User.query.all()` і використовуйте потрібні ID. Не створюйте дублікати username/email.

## 4. Додати теги (пункти 9–10)

У `flask shell`:

```python
from app.extensions import db
from app.posts.models import Post, Tag

python_tag = Tag(name="Python")
flask_tag = Tag(name="Flask")
web_tag = Tag(name="Web")
db.session.add_all([python_tag, flask_tag, web_tag])
db.session.commit()

posts = db.session.scalars(db.select(Post).order_by(Post.id)).all()
if posts:
    posts[0].tags.append(python_tag)
    posts[0].tags.append(flask_tag)
    if len(posts) > 1:
        posts[1].tags.append(python_tag)
        posts[1].tags.append(web_tag)
    db.session.commit()

print("Теги першого поста:", posts[0].tags if posts else [])
print("Пости з тегом Python:", python_tag.posts)
```

## 5. Форми та HTML (пункти 8, 11, 12)

У формі створення/редагування допису список авторів формується з таблиці `users`, а поле `tags` дозволяє вибрати кілька тегів. На сторінці допису теги показуються як стилізовані Bootstrap badges.

Щоб форма мала доступні варіанти, спочатку додайте користувачів і теги через shell. Перейдіть на `/post/create`.

## 6. Оптимізація завантаження (пункт 13)

Для підготовки п'яти дописів, двох авторів і трьох тегів створіть/перевірте дані у shell. Приклад створення відсутніх записів:

```python
from app.extensions import db
from app.posts.models import User, Post, Tag

u1 = db.session.scalar(db.select(User).where(User.username == "user1"))
u2 = db.session.scalar(db.select(User).where(User.username == "user2"))
if u1 is None:
    u1 = User(username="user1", email="user1@example.com", password="123456")
    db.session.add(u1)
if u2 is None:
    u2 = User(username="user2", email="user2@example.com", password="123456")
    db.session.add(u2)
for name in ["Python", "Flask", "Web"]:
    if db.session.scalar(db.select(Tag).where(Tag.name == name)) is None:
        db.session.add(Tag(name=name))
db.session.commit()

u1 = db.session.scalar(db.select(User).where(User.username == "user1"))
u2 = db.session.scalar(db.select(User).where(User.username == "user2"))
tags = db.session.scalars(db.select(Tag).order_by(Tag.id)).all()
for i in range(5):
    post = Post(title=f"Тестовий допис {i+1}", content="Текст для перевірки ORM-зв'язків", category="tech", user=u1 if i % 2 == 0 else u2)
    post.tags = [tags[i % len(tags)], tags[(i + 1) % len(tags)]]
    db.session.add(post)
db.session.commit()
```

У `app/__init__.py` перед `db.init_app(app)` можна тимчасово увімкнути SQL-логування:

```python
app.config["SQLALCHEMY_ECHO"] = True
```

Виконайте кожен варіант у новому запуску `flask shell`, щоб сесія була чистою. Перед підрахунком переконайтеся, що тестові дані вже збережені. Рахуйте лише SELECT під час отримання дописів і циклу.

### Варіант A — без eager loading

```python
from sqlalchemy import select
from app.extensions import db
from app.posts.models import Post

stmt = select(Post).order_by(Post.id.desc())
posts = db.session.scalars(stmt).all()
for post in posts:
    print(post.title, post.user.username, [tag.name for tag in post.tags])
```

### Варіант B — joinedload та selectinload

```python
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from app.extensions import db
from app.posts.models import Post

stmt = (
    select(Post)
    .options(joinedload(Post.user), selectinload(Post.tags))
    .order_by(Post.id.desc())
)
posts = db.session.scalars(stmt).all()
for post in posts:
    print(post.title, post.user.username, [tag.name for tag in post.tags])
```

### Таблиця для звіту

Кількість SELECT потрібно зафіксувати за SQL-журналом у власному запуску. Для набору з п'яти дописів, двох авторів та завантаження тегів кожного допису типовий результат без eager loading — 1 запит на дописи + до 2 запитів на авторів (кеш identity map) + 5 запитів на колекції тегів = до 8 SELECT. З `joinedload(Post.user)` і `selectinload(Post.tags)` типовий результат — 2 SELECT: один для дописів разом з авторами і один для всіх тегів вибраних дописів. Фактичні цифри вкажіть за журналом, бо вони залежать від кількості дописів, авторів і вже завантажених об'єктів.

| Варіант запиту | Кількість дописів | Кількість SELECT |
|---|---:|---:|
| Без `.options()` | Запишіть фактичну кількість | Запишіть із SQL-журналу |
| Із `joinedload()` та `selectinload()` | Запишіть фактичну кількість | Запишіть із SQL-журналу |

## 7. Перевірка

```bash
flask run
```

Відкрийте `/post/`, створіть допис з автором і кількома тегами, відкрийте його сторінку та перевірте відображення автора і тегів. Для звіту додайте власні скриншоти пунктів 7–13, два фрагменти коду оптимізації, результати виконання, SQL-журнал і заповнену таблицю.

> Примітка: пароль у цій навчальній моделі зберігається у полі `password` відповідно до умови лабораторної. Для реального застосунку паролі потрібно зберігати лише у вигляді криптографічного хешу.
