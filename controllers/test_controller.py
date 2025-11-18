from flask import Blueprint, jsonify
from models.db import db
from sqlalchemy import text

test_bp = Blueprint('test_bp', __name__)

@test_bp.route('/db')
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"db": "OK"})
    except Exception as e:
        return jsonify({"db": "ERROR", "error": repr(e)}), 500
