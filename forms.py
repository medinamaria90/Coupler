from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, \
    validators, IntegerField, SelectField, TextAreaField, \
    SelectMultipleField, widgets
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


LABELS = [
    'Deporte', 'Yoga', 'Senderismo', 'Viajes', 'Cocina', 'Fotografía', 'Arte', 'Libros',
    'Series', 'Cine', 'Teatro', 'Juegos de mesa', 'Voluntariado', 'Política',
    'Camping', 'Bicicleta', 'Salir de Fiesta', 'Tardeo', 'Debates', 'Jardinería',
    'Mascotas', 'Naturaleza', 'Moda', 'Meditación', 'Conciertos', 'Escritura', 'Ciencia',
    'Historia', 'Religión', 'Activismos', 'Escalada', 'Hijos', 'Gastronomía', 'Baile',
    'Filosofía', 'Manualidades', 'Arquitectura', 'Cultura', 'Restaurantes',
    'Espiritualidad', 'Psicología', 'Padel', 'Cafeterías', 'Museos', 'LGTBQIA+', 'Emprendimiento',
    'Aventuras','Crecimiento personal'
]

labels_form = []
for label in LABELS:
    label_element =(label,label)
    labels_form.append(label_element)

class MyProfile(FlaskForm):

    def __init__(self, *args, **kwargs):
        super(MyProfile, self).__init__(*args, **kwargs)
        self.meta = {"csrf": False, "autocomplete": "off"}  # Para evitar la generación automática del CSRF token

    name1 = StringField(label='', validators=[DataRequired(message="Data required")],  render_kw={"autocomplete": "off", "maxlength": 16, "placeholder": ""})
    name2 = StringField(label='', validators=[DataRequired(message="Data required")],  render_kw={"maxlength": 16, "placeholder": ""})
    age1 = IntegerField(label='', validators=[DataRequired(message="Data required"), validators.number_range(18, 99, message="La edad debe estar entre 18 y 99"),], render_kw={"placeholder": ""})
    age2 = IntegerField(label='', validators=[DataRequired(message="Data required"), validators.number_range(18, 99, message="La edad debe estar entre 18 y 99"),], render_kw={"placeholder": ""})
    gender1 = SelectField("Gender", choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('No binario', 'No binario'),
                                             ('Otros', 'Otros')])
    gender2= SelectField("Gender", choices=[('Hombre','Hombre'), ('Mujer','Mujer'), ('No binario','No binario'), ('Otros','Otros')])
    couple_description = TextAreaField(label='description',
                                       validators=[DataRequired(message="Es necesaria una descripción")],
                                       render_kw={"placeholder": "Descripción", "rows": 5, })
    tags = SelectMultipleField('Etiquetas', choices=LABELS,
                               widget=widgets.ListWidget(prefix_label=False),
                               option_widget=widgets.CheckboxInput())
    submit = SubmitField(label="Guardar")

