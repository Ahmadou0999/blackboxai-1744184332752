from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from app.forms.budget_forms import BudgetForm, LockBudgetForm
from app.services.budget_service import BudgetService
from app.models import Budget
from datetime import datetime, date
from app import db

bp = Blueprint('budget', __name__, url_prefix='/budgets')

@bp.route('/')
def index():
    # Get budgets sorted by date (newest first)
    budgets = Budget.query.order_by(Budget.date.desc()).all()
    return render_template('budget/index.html', budgets=budgets)

@bp.route('/new', methods=['GET', 'POST'])
def new():
    form = BudgetForm()
    if form.validate_on_submit():
        try:
            budget = BudgetService.create_budget(form)
            flash('Budget created successfully!', 'success')
            return redirect(url_for('budget.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating budget: {str(e)}', 'danger')
    
    return render_template('budget/form.html', form=form)

@bp.route('/<int:budget_id>', methods=['GET', 'POST'])
def view(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    lock_form = LockBudgetForm()
    
    if lock_form.validate_on_submit() and lock_form.confirm.data:
        try:
            BudgetService.lock_budget(budget_id)
            flash('Budget locked successfully!', 'success')
            return redirect(url_for('budget.view', budget_id=budget_id))
        except Exception as e:
            flash(f'Error locking budget: {str(e)}', 'danger')
    
    # Calculate remaining budget
    remaining = BudgetService.calculate_remaining(budget_id)
    
    return render_template('budget/view.html', 
                         budget=budget,
                         lock_form=lock_form,
                         remaining=remaining)

@bp.route('/api/remaining/<int:budget_id>')
def get_remaining(budget_id):
    remaining = BudgetService.calculate_remaining(budget_id)
    return jsonify({'remaining': remaining})

@bp.route('/api/lock/<int:budget_id>', methods=['POST'])
def lock(budget_id):
    try:
        budget = BudgetService.lock_budget(budget_id)
        return jsonify({'success': True, 'locked': budget.locked})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400