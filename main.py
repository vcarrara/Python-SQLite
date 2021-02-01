from flask import Flask, jsonify, request, abort
from db_connection import retrieve_companies, count_posts, retrieve_posts, retrieve_interactions
import re

app = Flask(__name__)


@app.route('/companies')
def companies():
    return jsonify(retrieve_companies())


@app.route('/countPosts')
def count_posts():
    company_id = request.args.get('companyId')
    source = request.args.get('source')
    if (company_id is None):
        abort(400)
    return jsonify(count_posts(company_id, source))


@app.route('/posts')
def posts():
    company_id = request.args.get('companyId')
    source = request.args.get('source')
    if company_id is None or source is None:
        abort(400)
    return jsonify(retrieve_posts(company_id, source))


@app.route('/interactions')
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


if __name__ == "__main__":
    app.run(debug=True)
