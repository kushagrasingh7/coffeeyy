from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL

class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    map_url = StringField('Map URL', validators=[DataRequired(), URL()])
    image_url = StringField('Image URL', validators=[DataRequired(), URL()])
    seating_capacity = StringField('Seating Capacity', validators=[DataRequired()])
    has_toilet = BooleanField('Has Toilet')
    has_wifi = BooleanField('Has WiFi')
    has_power_outlets = BooleanField('Has Power Outlets')
    can_take_calls = BooleanField('Can Take Calls')
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search_query = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Search for a cafe"})
    submit = SubmitField('Submit')
