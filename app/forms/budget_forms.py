from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date
from wtforms.widgets import html5

class BudgetForm(FlaskForm):
    date = DateField('Date', 
                    validators=[DataRequired()],
                    default=date.today,
                    widget=html5.DateInput())
    
    amount = FloatField('Budget Amount', 
                       validators=[DataRequired(), NumberRange(min=0.01)],
                       render_kw={"step": "0.01"})
    
    check_number = StringField('Check Number',
                             validators=[Optional()])
    
    carryover = BooleanField('Include Previous Day Remaining',
                           default=True,
                           description="Automatically add remaining from previous day")
    
    submit = SubmitField('Save Budget')

class LockBudgetForm(FlaskForm):
    confirm = BooleanField('I confirm I want to lock this day',
                         validators=[DataRequired()])
    submit = SubmitField('Lock Day')