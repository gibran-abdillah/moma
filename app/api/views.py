from app.api import api_blueprint
from flask import jsonify, request
from app.models import Money , DEFAULT_MONTHS


@api_blueprint.route('/getData')
def getData():
    try:
        month = int(request.args.get('month', DEFAULT_MONTHS))
        return jsonify(Money.fetch_data(month))
    except Exception as e:
        return jsonify(Money.fetch_data(DEFAULT_MONTHS))


@api_blueprint.route('/')
def api_index():
    return jsonify([data.to_dict() for id, data in enumerate(Money.query.all())])

