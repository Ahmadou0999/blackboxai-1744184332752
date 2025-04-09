from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import html5

class DestinationForm(FlaskForm):
    code = StringField('Destination Code (e.g. KL, FK)',
                     validators=[DataRequired()],
                     render_kw={"maxlength": "10"})
    
    name = StringField('Destination Name',
                      validators=[DataRequired()])
    
    road_cost = FloatField('Standard Road Cost',
                         validators=[Optional(), NumberRange(min=0)],
                         render_kw={"step": "0.01"})
    
    ferry_cost = FloatField('Standard Ferry Cost',
                          validators=[Optional(), NumberRange(min=0)],
                          render_kw={"step": "0.01"})
    
    station_cost = FloatField('Standard Station Cost',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"step": "0.01"})
    
    customs_cost = FloatField('Standard Customs Cost',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"step": "0.01"})
    
    misc_cost = FloatField('Standard Miscellaneous Cost',
                         validators=[Optional(), NumberRange(min=0)],
                         render_kw={"step": "0.01"})
    
    submit = SubmitField('Save Destination')

class DestinationCostUpdateForm(FlaskForm):
    road_cost = FloatField('New Road Cost',
                         validators=[Optional(), NumberRange(min=0)],
                         render_kw={"step": "0.01"})
    
    ferry_cost = FloatField('New Ferry Cost',
                          validators=[Optional(), NumberRange(min=0)],
                          render_kw={"step": "0.01"})
    
    station_cost = FloatField('New Station Cost',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"step": "0.01"})
    
    customs_cost = FloatField('New Customs Cost',
                            validators=[Optional(), NumberRange(min=0)],
                            render_kw={"step": "0.01"})
    
    misc_cost = FloatField('New Miscellaneous Cost',
                         validators=[Optional(), NumberRange(min=0)],
                         render_kw={"step": "0.01"})
    
    submit = SubmitField('Update Costs')