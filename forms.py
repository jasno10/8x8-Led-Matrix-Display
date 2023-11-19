from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class homeForm(FlaskForm):
    arraybox = StringField('Array')
    reset_btn = SubmitField('Reset')
    apply_btn = SubmitField('Apply')

class characterForm(FlaskForm):
    characterbox = StringField('Enter character', validators=[DataRequired(), Length(max=1)])
    apply_btn = SubmitField('Apply')

class addcharacterForm(FlaskForm):
    character = StringField('Character', validators=[DataRequired(), Length(max=1)])
    submit_btn = SubmitField('Apply')

class drawingForm(FlaskForm):
    dropdown = SelectField('Select Pattern', choices=[
        ('', 'Select Drawing'),
        ('checkered-id', 'Checkered'),
        ('square-id', 'Square')
    ])
    apply_btn = SubmitField('Apply')

class addDrawingForm(FlaskForm):
    drawingName = StringField('Enter Drawing Name', validators=[DataRequired(), Length(max=24)])
    save_btn = SubmitField('Apply')
    cancel_btn = SubmitField('Cancel')

class messageForm(FlaskForm):
    messagebox = StringField('Enter message', validators=[DataRequired(), Length(max=15)])
    apply_btn = SubmitField('Apply')

class settingsForm(FlaskForm):
    shutdown_btn = SubmitField('Shutdown')


