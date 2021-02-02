from flask import Flask, jsonify, request, abort
from db_connection import retrieve_companies, retrieve_count_posts, retrieve_posts, retrieve_interactions, retrieve_evolution
import re
import os

app = Flask(__name__)


@app.route('/companies', methods=['GET'])
def companies():
    return jsonify(retrieve_companies())


@app.route('/countPosts', methods=['GET'])
def count_posts():
    company_id = request.args.get('companyId')
    source = request.args.get('source')
    if (not company_id):
        abort(400, 'Bad request: companyId must be specified')
    return jsonify(retrieve_count_posts(company_id, source))


@app.route('/posts', methods=['GET'])
def posts():
    company_id = request.args.get('companyId')
    source = request.args.get('source')
    if not company_id or not source:
        abort(400, 'Bad request: companyId and source must be specified')
    return jsonify(retrieve_posts(company_id, source))


@app.route('/interactions', methods=['GET'])
def interactions():
    company_id = request.args.get('companyId')
    min_date = request.args.get('minDate')
    max_date = request.args.get('maxDate')
    preg = '^\\d{4}-\\d{2}-\\d{2}$'
    if not company_id:
        abort(400, 'Bad request: companyId must be specified')
    if min_date:
        if not re.search(preg, min_date):
            abort(400, 'Bad request: minDate must have pattern YYYY-MM-DD')
    if max_date:
        if not re.search(preg, max_date):
            abort(400, 'Bad request: maxDate must have pattern YYYY-MM-DD')
    return jsonify(retrieve_interactions(company_id, min_date, max_date))


@app.route('/evolution', methods=['GET'])
def evolution():
    company_id = request.args.get('companyId')
    if not company_id:
        abort(400, 'Bad request: companyId must be specified')
    return jsonify(retrieve_evolution(company_id))


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('PORT'), host="0.0.0.0")
