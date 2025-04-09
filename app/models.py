from datetime import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_property

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)
    check_number = db.Column(db.String(50))
    remaining = db.Column(db.Float, default=0.0)
    locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    assignments = db.relationship('Assignment', backref='budget', lazy=True, cascade='all, delete-orphan')
    manual_expenses = db.relationship('ManualExpense', backref='budget', lazy=True, cascade='all, delete-orphan')

    @hybrid_property
    def total_expenses(self):
        return sum(a.total_cost for a in self.assignments) + sum(me.amount for me in self.manual_expenses)

class Destination(db.Model):
    __tablename__ = 'destinations'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # KL, FK, DK etc.
    name = db.Column(db.String(100), unique=True, nullable=False)
    road_cost = db.Column(db.Float, default=0.0)
    ferry_cost = db.Column(db.Float, default=0.0)
    station_cost = db.Column(db.Float, default=0.0)
    customs_cost = db.Column(db.Float, default=0.0)
    misc_cost = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @hybrid_property
    def total_cost(self):
        return self.road_cost + self.ferry_cost + self.station_cost + self.customs_cost + self.misc_cost

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    category = db.Column(db.Enum('Fuel', 'Diesel', 'Passenger', 'Cargo'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    assignments = db.relationship('Assignment', backref='vehicle', lazy=True)

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    driver = db.Column(db.String(100), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    road_cost = db.Column(db.Float)
    ferry_cost = db.Column(db.Float)
    station_cost = db.Column(db.Float)
    customs_cost = db.Column(db.Float)
    misc_cost = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @hybrid_property
    def total_cost(self):
        return (self.road_cost or 0) + (self.ferry_cost or 0) + (self.station_cost or 0) + (self.customs_cost or 0) + (self.misc_cost or 0)

class ManualExpense(db.Model):
    __tablename__ = 'manual_expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.Enum('Washing', 'Breakdown', 'Equipment', 'Other'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)