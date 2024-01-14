from flask import Flask,abort, jsonify, make_response, request

from models import movies

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.route("/api/v1/movies/", methods=["GET"])
def movies_list_api_v1():
    return jsonify(movies.all())

@app.route("/api/v1/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    return jsonify({"movie": movie})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.route("/api/v1/movies/", methods=["POST"])
def create_movie():
    if not request.json or not 'title' in request.json:
        abort(400)
    movie = {
        'id': movies.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'author': request.json['author'],
        'description': request.json.get('description', ""),
        'Watched?': False
    }
    movies.create(movie)
    return jsonify({'movie': movie}), 201

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

@app.route("/api/v1/movies/<int:movie_id>", methods=['DELETE'])
def delete_movie(movie_id):
    result = movies.delete(movie_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'author' in data and not isinstance(data.get('author'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'Watched?' in data and not isinstance(data.get('Watched?'), bool)
    ]):
        abort(400)
    movie = {
        'title': data.get('title', movie['title']),
        'description': data.get('description', movie['description']),
        'Watched?': data.get('Watched?', movie['Watched?'])
    }
    movies.update(movie_id, movie)
    return jsonify({'movie': movie})

if __name__ == "__main__":
    app.run(debug=True)