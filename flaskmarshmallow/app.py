from flask import Flask, request, jsonify, make_response
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from SQLALCHEMY_DATABASE_URI import SQLALCHEMY_DATABASE_URI


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialisation = db.Column(db.String(50))

    def __init__(self, name, specialisation):
        self.name = name
        self.specialisation = specialisation

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Product %d>' % self.id


db.create_all()


class AuthorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Authors
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    specialisation = fields.String(required=True)


@app.route('/authors', methods=['GET'])
def index():
    all_authors = Authors.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(all_authors)
    return make_response(jsonify({"authors": authors}))


@app.route('/authors/<id>', methods=['GET'])
def get_author_by_id(id):
    get_author = Authors.query.get(id)
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))


@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    author_schema = AuthorSchema()
    author = author_schema.load(data)
    result = author_schema.dump(author.create()).data
    return make_response(jsonify({'author': author}), 201)


@app.route('/authors/<id>', methods=['PUT'])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Authors.query.get(id)
    if data.get('specialisation'):
        get_author.specialisation = data['specialisation']
    if data.get('name'):
        get_author.specialisation = data['name']
    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema(only=['id', 'name', 'specialisation'])
    author = author_schema.dump(get_author)
    return make_response(jsonify({"author": author}))


@app.route('/authors/<id>', methods=['DELETE'])
def delete_author_by_id(id):
    get_author = Authors.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response("", 204)


if __name__ == "__main__":
    app.run(debug=True)
