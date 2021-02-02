from flask import Flask, jsonify, request, abort
from db_connection import retrieve_companies, retrieve_count_posts, retrieve_posts, retrieve_interactions, retrieve_evolution
import re

app = Flask(__name__)


@app.route('/companies', methods=['GET'])
def companies():
    return jsonify(retrieve_companies())


@app.route('/countPosts', methods=['GET'])
def count_posts():
    company_id = request.args.get('companyId')
    source = request.args.get('source')
    if (company_id is None):
        abort(400)
    return jsonify(retrieve_count_posts(company_id, source))


@app.route('/posts', methods=['GET'])
def posts():
    company_id = request.args.get('companyId')
    source = request.args.get('source')
    if company_id is None or source is None:
        abort(400)
    return jsonify(retrieve_posts(company_id, source))


@app.route('/interactions', methods=['GET'])
def interactions():
    company_id = request.args.get('companyId')
    min_date = request.args.get('minDate')
    max_date = request.args.get('maxDate')
    preg = '^\\d{4}-\\d{2}-\\d{2}$'
    if company_id is None:
        abort(400)
    if min_date is not None:
        if re.search(preg, min_date) is None:
            abort(400)
    if max_date is not None:
        if re.search(preg, max_date) is None:
            abort(400)
    return jsonify(retrieve_interactions(company_id, min_date, max_date))


@app.route('/evolution', methods=['GET'])
def evolution():
    company_id = request.args.get('companyId')
    if (company_id is None):
        abort(400)
    return jsonify(retrieve_evolution(company_id))


if __name__ == "__main__":
    app.run(debug=True, port=80)
