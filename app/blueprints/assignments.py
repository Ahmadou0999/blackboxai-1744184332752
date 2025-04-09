from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.forms.assignment_forms import AssignmentForm, AssignmentFilterForm
from app.services.assignment_service import AssignmentService
from app.services.budget_service import BudgetService
from app.models import Assignment, Budget, Vehicle, Destination
from datetime import date, timedelta
from app import db

bp = Blueprint('assignments', __name__, url_prefix='/assignments')

@bp.route('/')
def index():
    form = AssignmentFilterForm()
    date_filter = request.args.get('date_filter', 'today')
    
    assignments = AssignmentService.get_assignments_by_date(date_filter)
    return render_template('assignments/index.html', 
                         assignments=assignments,
                         form=form,
                         date_filter=date_filter)

@bp.route('/new/<int:budget_id>', methods=['GET', 'POST'])
def new(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.locked:
        flash('This budget is locked and cannot be modified', 'danger')
        return redirect(url_for('budget.view', budget_id=budget_id))
    
    form = AssignmentForm()
    form.vehicle.choices = [(v.id, f"{v.number} ({v.category})") 
                           for v in Vehicle.query.order_by(Vehicle.category, Vehicle.number).all()]
    form.destination.choices = [(d.id, f"{d.code} - {d.name}") 
                              for d in Destination.query.order_by(Destination.code).all()]
    
    if form.validate_on_submit():
        try:
            assignment = AssignmentService.create_assignment(budget_id, form)
            BudgetService.calculate_remaining(budget_id)
            flash('Assignment created successfully!', 'success')
            return redirect(url_for('budget.view', budget_id=budget_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating assignment: {str(e)}', 'danger')
    
    return render_template('assignments/form.html', 
                         form=form,
                         budget=budget)

@bp.route('/<int:assignment_id>/edit', methods=['GET', 'POST'])
def edit(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.budget.locked:
        flash('This assignment is locked and cannot be modified', 'danger')
        return redirect(url_for('budget.view', budget_id=assignment.budget_id))
    
    form = AssignmentForm(obj=assignment)
    form.vehicle.choices = [(v.id, f"{v.number} ({v.category})") 
                           for v in Vehicle.query.order_by(Vehicle.category, Vehicle.number).all()]
    form.destination.choices = [(d.id, f"{d.code} - {d.name}") 
                              for d in Destination.query.order_by(Destination.code).all()]
    
    if form.validate_on_submit():
        try:
            assignment = AssignmentService.update_assignment(assignment_id, form)
            BudgetService.calculate_remaining(assignment.budget_id)
            flash('Assignment updated successfully!', 'success')
            return redirect(url_for('budget.view', budget_id=assignment.budget_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating assignment: {str(e)}', 'danger')
    
    return render_template('assignments/form.html', 
                         form=form,
                         budget=assignment.budget)

@bp.route('/<int:assignment_id>/delete', methods=['POST'])
def delete(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    if assignment.budget.locked:
        flash('This assignment is locked and cannot be modified', 'danger')
        return redirect(url_for('budget.view', budget_id=assignment.budget_id))
    
    try:
        AssignmentService.delete_assignment(assignment_id)
        BudgetService.calculate_remaining(assignment.budget_id)
        flash('Assignment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting assignment: {str(e)}', 'danger')
    
    return redirect(url_for('budget.view', budget_id=assignment.budget_id))

@bp.route('/api/destination/<int:destination_id>/costs')
def get_destination_costs(destination_id):
    costs = AssignmentService.get_destination_costs(destination_id)
    if not costs:
        return jsonify({'error': 'Destination not found'}), 404
    return jsonify(costs)