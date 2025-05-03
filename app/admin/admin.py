from datetime import datetime
from sqladmin import Admin, ModelView

from app.models.user import User
from app.models.category import Category
from app.models.article import Article
from app.database import engine


def format_datetime(value: datetime | None) -> str:
    """Форматирование даты для отображения в админ-панели."""
    return value.strftime('%Y-%m-%d %H:%M') if value else ''


class UserAdmin(ModelView, model=User):
    """Админ-панель для управления пользователями."""
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'

    column_labels = {
        'id': 'ID пользователья',
        'username': 'Имя',
        'avatar': 'Аватар',
        'email': 'Email',
        'hashed_password': 'Парль',
        'bio': 'О себе',
        'is_banned': 'Бан',
        'is_admin': 'Администратор',
        'created_at': 'Дата регистрации',
        'articles': 'Статьи'
    }

    column_list = ['username', 'email', 'is_admin', 'is_banned']
    column_searchable_list = ['username', 'email']
    column_sortable_list = ['username', 'created_at', 'is_banned']
    column_formatters = {
        'created_at': lambda m, _: format_datetime(m.created_at),
        'is_admin': lambda m, _: '✅' if m.is_admin else '❌',
        'is_banned': lambda m, _: '✅' if m.is_banned else '❌'
    }

    form_widget_args = {'created_at': {'readonly': True}}

    edit_template = "sqladmin/custom_edit.html"
    create_template = "sqladmin/custom_create.html"


class CategoryAdmin(ModelView, model=Category):
    """Админ-панель для управления категориями."""
    name = 'Категория'
    name_plural = 'Категории'
    icon = 'fa-solid fa-list'

    column_labels = {
        'id': 'ID категории',
        'title': 'Название',
        'title_img': 'Титульная картинка',
        'description': 'Краткое описание',
        'articles': 'Статьи',
        'created_at': 'Дата создания',
        'is_published': 'Опубликовать'
    }

    column_list = ['title', 'description', 'is_published']
    column_searchable_list = ['title']
    column_sortable_list = ['title', 'is_published']
    column_formatters = {
        'created_at': lambda m, _: format_datetime(m.created_at),
        'is_published': lambda m, _: '✅' if m.is_published else '❌'
    }

    form_widget_args = {'created_at': {'readonly': True}}


class ArticleAdmin(ModelView, model=Article):
    """Админ-панель для управления статьями."""
    name = 'Статья'
    name_plural = 'Статьи'
    icon = 'fa-solid fa-newspaper'

    column_labels = {
        'id': 'ID статьи',
        'title': 'Название',
        'title_img': 'Титульная картинка',
        'description': 'Краткое описание',
        'content': 'Содержание',
        'audio': 'Аудио-подкаст',
        'video': 'Видео-подкаст',
        'author': 'Автор',
        'author_id': 'ID автора',
        'category': 'Категория',
        'category_id': 'ID категории',
        'created_at': 'Дата создания',
        'updated': 'Обновление',
        'is_published': 'Опубликовано'
    }

    column_list = ['title',  'author', 'is_published', 'created_at', 'updated']
    column_searchable_list = ['title']
    column_sortable_list = ['title', 'created_at', 'is_published']
    column_formatters = {
        'created_at': lambda m, _: format_datetime(m.created_at),
        'updated': lambda m, _: '✅' if m.updated else '❌',
        'author': lambda m, _: m.author.username if m.author else "Администратор",
        'is_published': lambda m, _: '✅' if m.is_published else '❌'
    }

    form_widget_args = {'created_at': {'readonly': True}}

    edit_template = "sqladmin/custom_edit.html"
    create_template = "sqladmin/custom_create.html"


def init_admin(app):
    """Инициализация админ-панели."""
    admin = Admin(
        app=app,
        engine=engine,
        title='Admin Work Panel',
        base_url='/admin',
        templates_dir='app/templates',
        logo_url='/static/img/logo/logo.svg',
        favicon_url="/static/img/favicon/favicon.ico",
    )
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ArticleAdmin)
