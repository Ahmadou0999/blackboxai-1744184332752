from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import html5

class AssignmentForm(FlaskForm):
    vehicle = SelectField('Vehicle', 
                        coerce=int,
                        validators=[DataRequired()],
                        render_kw={"class": "select2"})
    
    driver = StringField('Driver Name',
                       validators=[DataRequired()])
    
    destination = SelectField('Destination',
                            coerce=int,
                            validators=[DataRequired()],
                            render_kw={"class": "select2"})
    
    # Cost fields will be auto-populated via JavaScript
    road_cost = FloatField('Road Cost',
                         validators=[Optional(), NumberRange(min=0)],
                         render_kw={"readonly": True, "step": "0.01"})
    
    ferry_cost = FloatField('Ferry Cost',
                          validators=[Optional(), NumberRange(min=0)],
                          render_kw={"readonly": True, "step": "0.01"})
    
    station_cost = FloatField('Station Cost',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"readonly": True, "step": "0.01"})
    
    customs_cost = FloatField('Customs Cost',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"readonly": True, "step": "0.01"})
    
    misc_cost = FloatField('Miscellaneous Cost',
                         validators=[Optional(), NumberRange(min=0)],
                         render_kw={"step": "0.01"})
    
    submit = SubmitField('Save Assignment')

class AssignmentFilterForm(FlaskForm):
    vehicle_category = SelectField('Vehicle Category',
                                 choices=[('', 'All'), ('Fuel', 'Fuel'), ('Diesel', 'Diesel')],
                                 validators=[Optional()])
    
    date_range = StringField('Date Range',
                           validators=[Optional()],
                           render_kw={"class": "daterangepicker"})
    
    submit = SubmitField('Filter')