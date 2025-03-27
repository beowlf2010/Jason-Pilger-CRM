from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Lead, db
import pandas as pd
import os

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    leads = Lead.query.all()
    return render_template('dashboard.html', leads=leads)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_csv(file)
            for _, row in df.iterrows():
                existing = Lead.query.filter_by(name=row['name'], phone=row['phone']).first()
                if not existing:
                    lead = Lead(
                        name=row['name'],
                        phone=row['phone'],
                        status=row.get('status', 'Active'),
                        source=row.get('source', ''),
                        salesperson=row.get('salesperson', '')
                    )
                    db.session.add(lead)
            db.session.commit()
            flash('Leads imported successfully.')
            return redirect(url_for('main.dashboard'))
    return render_template('upload.html')

@main.route('/lead/<int:id>')
@login_required
def lead_detail(id):
    lead = Lead.query.get_or_404(id)
    return render_template('lead_detail.html', lead=lead)
