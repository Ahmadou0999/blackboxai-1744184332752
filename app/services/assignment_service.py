from app import db
from app.models import Assignment, Destination, Vehicle, Budget
from datetime import date

class AssignmentService:
    @staticmethod
    def create_assignment(budget_id, form_data):
        """Create a new assignment with auto-populated costs"""
        # Get related objects
        budget = Budget.query.get(budget_id)
        if not budget or budget.locked:
            raise ValueError("Budget not found or locked")

        destination = Destination.query.get(form_data.destination.data)
        vehicle = Vehicle.query.get(form_data.vehicle.data)

        # Create new assignment
        assignment = Assignment(
            budget_id=budget_id,
            vehicle_id=vehicle.id,
            driver=form_data.driver.data,
            destination_id=destination.id,
            road_cost=destination.road_cost,
            ferry_cost=destination.ferry_cost,
            station_cost=destination.station_cost,
            customs_cost=destination.customs_cost,
            misc_cost=form_data.misc_cost.data or 0
        )

        db.session.add(assignment)
        db.session.commit()
        return assignment

    @staticmethod
    def update_assignment(assignment_id, form_data):
        """Update an existing assignment"""
        assignment = Assignment.query.get(assignment_id)
        if not assignment or assignment.budget.locked:
            raise ValueError("Assignment not found or budget locked")

        # Update fields
        assignment.driver = form_data.driver.data
        assignment.misc_cost = form_data.misc_cost.data or 0
        
        # Update destination if changed
        if form_data.destination.data != assignment.destination_id:
            new_dest = Destination.query.get(form_data.destination.data)
            assignment.destination_id = new_dest.id
            assignment.road_cost = new_dest.road_cost
            assignment.ferry_cost = new_dest.ferry_cost
            assignment.station_cost = new_dest.station_cost
            assignment.customs_cost = new_dest.customs_cost

        db.session.commit()
        return assignment

    @staticmethod
    def delete_assignment(assignment_id):
        """Delete an assignment"""
        assignment = Assignment.query.get(assignment_id)
        if not assignment or assignment.budget.locked:
            raise ValueError("Assignment not found or budget locked")

        db.session.delete(assignment)
        db.session.commit()
        return True

    @staticmethod
    def get_destination_costs(destination_id):
        """Get standard costs for a destination"""
        destination = Destination.query.get(destination_id)
        if not destination:
            return None

        return {
            'road_cost': destination.road_cost,
            'ferry_cost': destination.ferry_cost,
            'station_cost': destination.station_cost,
            'customs_cost': destination.customs_cost,
            'misc_cost': destination.misc_cost,
            'total_cost': destination.total_cost
        }

    @staticmethod
    def get_assignments_by_date(date_filter):
        """Get assignments filtered by date"""
        query = Assignment.query.join(Budget)
        
        if date_filter == 'today':
            today = date.today()
            query = query.filter(Budget.date == today)
        elif date_filter == 'week':
            start_date = date.today() - timedelta(days=7)
            query = query.filter(Budget.date >= start_date)
        
        return query.order_by(
            Vehicle.category,
            Vehicle.number
        ).all()