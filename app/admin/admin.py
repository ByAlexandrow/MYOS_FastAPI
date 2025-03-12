from sqladmin import Admin, ModelView

from app.database import engine

from app.models.category import Category
from app.models.article import Article, Carousel
from app.models.user import SuperUser


def setup_admin(app):
    class SuperUserAdmin(ModelView, model=SuperUser):
        column_list = [SuperUser.id, SuperUser.username]
        column_searchable_list = [SuperUser.username]
        column_labels = {
            SuperUser.username: 'Имя Админа',
        }
        name = 'Админ'
        name_plural = 'Админы'


    class CategoryAdmin(ModelView, model=Category):
        column_list = [Category.id, Category.title, Category.description, Category.is_published]
        column_searchable_list = [Category.title, Category.is_published]
        column_labels = {
            Category.title: 'Название',
            Category.cover_img: 'Титульная картинка',
            Category.description: 'Описание',
            Category.is_published: 'Публикация',
        }
        name = 'Категория'
        name_plural = 'Категории'


    class ArticleAdmin(ModelView, model=Article):
        column_list = [
            Article.id, Article.title, Article.description, Article.category_id, Article.is_published
        ]
        column_searchable_list = [Article.title, Article.category_id, Article.is_published]
        column_labels = {
            Article.title: 'Название',
            Article.cover_img: 'Титульная картинка',
            Article.description: 'Описание',
            Article.content: 'Текст',
            Article.pdf: 'PDF',
            Article.category_id: 'Категория',
            Article.is_published: 'Публикация',
        }
        name = 'Статья'
        name_plural = 'Статьи'


    class CarouselAdmin(ModelView, model=Carousel):
        column_list = [Carousel.id, Carousel.title, Carousel.article_id, Carousel.is_published]
        column_searchable_list = [Carousel.title]
        column_labels = {
            Carousel.title: 'Название',
            Carousel.article_id: 'Статья',
            Carousel.is_published: 'Публикация',
        }
        name = 'Карусель'
        name_plural = 'Карусели'


    admin = Admin(app, engine)
    admin.add_view(SuperUserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ArticleAdmin)
    admin.add_view(CarouselAdmin)
