from datetime import date, timedelta
from app import db
from app.models import Budget, Assignment, ManualExpense

class BudgetService:
    @staticmethod
    def create_budget(form_data):
        """Create a new budget with carryover calculation"""
        new_budget = Budget(
            date=form_data.date.data,
            amount=form_data.amount.data,
            check_number=form_data.check_number.data
        )

        if form_data.carryover.data:
            previous_budget = Budget.query.filter(
                Budget.date < form_data.date.data
            ).order_by(Budget.date.desc()).first()

            if previous_budget:
                new_budget.remaining = previous_budget.remaining
                new_budget.amount += previous_budget.remaining

        db.session.add(new_budget)
        db.session.commit()
        return new_budget

    @staticmethod
    def lock_budget(budget_id):
        """Lock a budget to prevent modifications"""
        budget = Budget.query.get(budget_id)
        if not budget:
            return None

        budget.locked = True
        db.session.commit()
        return budget

    @staticmethod
    def calculate_remaining(budget_id):
        """Recalculate remaining budget"""
        budget = Budget.query.get(budget_id)
        if not budget:
            return None

        total_expenses = (
            sum(a.total_cost for a in budget.assignments) +
            sum(m.amount for m in budget.manual_expenses)
        )
        budget.remaining = budget.amount - total_expenses
        db.session.commit()
        return budget.remaining

    @staticmethod
    def get_daily_report(report_date):
        """Generate daily report data"""
        budget = Budget.query.filter_by(date=report_date).first()
        if not budget:
            return None

        return {
            'budget': budget,
            'assignments': sorted(
                budget.assignments,
                key=lambda a: (a.vehicle.category != 'Fuel', 
                              a.vehicle.category != 'Diesel',
                              a.vehicle.number)
            ),
            'manual_expenses': budget.manual_expenses,
            'total_expenses': sum(
                a.total_cost for a in budget.assignments
            ) + sum(
                m.amount for m in budget.manual_expenses
            )
        }