// Budget management functions - version 2.0
document.addEventListener('DOMContentLoaded', function() {
    console.log('Budget management initialized');
    
    // Verify CSRF token exists
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (!csrfToken) console.error('CSRF token not found!');

    // Delete assignment handler
    window.deleteAssignment = function(id) {
        if (confirm('Delete this assignment?')) {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/assignments/${id}/delete`;
            
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = '_csrf_token';
            csrfInput.value = csrfToken;
            
            form.appendChild(csrfInput);
            document.body.appendChild(form);
            form.submit();
        }
    };

    // Delete expense handler
    window.deleteExpense = function(id) {
        if (confirm('Delete this expense?')) {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/budgets/expenses/${id}/delete`;
            
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = '_csrf_token';
            csrfInput.value = csrfToken;
            
            form.appendChild(csrfInput);
            document.body.appendChild(form);
            form.submit();
        }
    };

    // Update remaining budget
    function updateBudget() {
        const budgetId = document.currentScript.dataset.budgetId;
        fetch(`/budgets/api/remaining/${budgetId}`)
            .then(response => response.json())
            .then(data => {
                const el = document.querySelector('.remaining-display');
                if (el) {
                    el.textContent = `$${data.remaining.toFixed(2)}`;
                    el.classList.toggle('text-danger', data.remaining < 0);
                }
            })
            .catch(err => console.error('Budget update failed:', err));
    }

    // Initialize periodic updates if budget is open
    if (document.currentScript.dataset.locked === 'false') {
        setInterval(updateBudget, 30000);
        updateBudget(); // Initial update
    }
});