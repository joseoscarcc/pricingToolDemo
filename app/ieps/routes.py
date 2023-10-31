from flask import render_template
from app.models.auth import login_required
from app.ieps import bp

@bp.route('/')
@login_required
def index():
    return render_template('ieps.html')