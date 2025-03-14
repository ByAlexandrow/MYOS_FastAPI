from wtforms import Form, FileField
from wtforms.validators import InputRequired


class CategoryForm(Form):
    cover_img = FileField('Титульная картинка', validators=[InputRequired()])

