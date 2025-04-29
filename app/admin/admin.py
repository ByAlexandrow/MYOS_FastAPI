from datetime import datetime
from sqladmin import Admin, ModelView

from app.models.user import User
from app.models.article import Article
from app.database import engine

from fastapi import Request
from sqladmin import ModelView
from wtforms import FileField
from pathlib import Path
import os
import uuid
from PIL import Image
from io import BytesIO
from typing import Dict, Any
from typing import Optional


def format_datetime(value: datetime | None) -> str:
    """Форматирование даты для отображения в админ-панели."""
    return value.strftime('%Y-%m-%d %H:%M') if value else ''


class UserAdmin(ModelView, model=User):
    """Админ-панель для управления пользователями."""
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'

    column_labels = {
        'id': 'ID',
        'username': 'Имя',
        'avatar': 'Аватар',
        'email': 'Email',
        'hashed_password': 'Парль',
        'bio': 'О себе',
        'is_admin': 'Администратор',
        'created_at': 'Дата регистрации',
        'articles': 'Статьи'
    }

    column_list = ['username', 'email', 'is_admin']
    column_searchable_list = ['username', 'email']
    column_sortable_list = ['username', 'created_at']
    column_formatters = {
        'created_at': lambda m, _: format_datetime(m.created_at),
        'is_admin': lambda m, _: '✅' if m.is_admin else '❌'
    }


class ArticleAdmin(ModelView, model=Article):
    """Админ-панель для управления статьями."""
    name = 'Статья'
    name_plural = 'Статьи'
    icon = 'fa-solid fa-newspaper'

    column_labels = {
        'id': 'ID',
        'title': 'Название',
        'title_img': 'Титульная картинка',
        'description': 'Краткое описание',
        'content': 'Содержание',
        'audio': 'Аудио-подкаст',
        'video': 'Видео-подкаст',
        'author': 'Автор',
        'author_id': 'ID автора',
        'created_at': 'Дата создания',
        'updated_on': 'Дата обновления',
        'is_published': 'Опубликовано'
    }

    column_list = ['title',  'author', 'is_published', 'created_at']
    column_searchable_list = ['title']
    column_sortable_list = ['title', 'created_at']
    column_formatters = {
        'created_at': lambda m, _: format_datetime(m.created_at),
        'updated_on': lambda m, _: format_datetime(m.updated_on),
        'author': lambda m, _: m.author.username if m.author else "Администратор",
        'is_published': lambda m, _: '✅' if m.is_published else '❌'
    }


def init_admin(app):
    """Инициализация админ-панели."""
    admin = Admin(
        app=app,
        engine=engine,
        title='Admin Work Panel',
        base_url='/admin',
        templates_dir='templates/admin',
        logo_url='/static/img/logo/logo.svg',
        favicon_url="/static/img/favicon/favicon.ico"
    )
    admin.add_view(UserAdmin)
    admin.add_view(ArticleAdmin)
