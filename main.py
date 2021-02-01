from flask import Flask, jsonify, request, abort
from db_connection import retrieve_companies, count_posts, retrieve_posts, retrieve_interactions
import re

app = Flask(__name__)


@app.route('/companies')
def companies():
    return jsonify(retrieve_companies())


@app.route('/countPosts')
def countPosts():
    companyId = request.args.get('companyId')
    source = request.args.get('source')
    if (companyId is None):
        abort(400)
    return jsonify(count_posts(companyId, source))


@app.route('/posts')
def posts():
    companyId = request.args.get('companyId')
    source = request.args.get('source')
    if companyId is None or source is None:
        abort(400)
    return jsonify(retrieve_posts(companyId, source))


@app.route('/interactions')
def interactions():
    companyId = request.args.get('companyId')
    minDate = request.args.get('minDate')
    maxDate = request.args.get('maxDate')
    preg = '^\\d{4}-\\d{2}-\\d{2}$'
    if companyId is None:
        abort(400)
    if minDate is not None:
        if re.search(preg, minDate) is None:
            abort(400)
    if maxDate is not None:
        if re.search(preg, maxDate) is None:
            abort(400)
    return jsonify(retrieve_interactions(companyId, minDate, maxDate))


if __name__ == "__main__":
    app.run(debug=True)
