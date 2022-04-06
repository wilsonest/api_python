from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  # IMPORTACION DE TODAS LAS LIBRERIAS NECESARIAS
from flask_marshmallow import Marshmallow
from config import config

app = Flask(__name__) # INSTANCIAR
#CONFIGURACION DE LA BD (URI) 
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/videos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

#DEFINICION LOS ATRIBUTOS PARA LA DB
class videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description
#CREACION DE TABLAS       
db.create_all()
#CREACION DE LOS ESQUEMAS CON MARSHMALLOW
class videoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

video_schema = videoSchema()
videos_schema = videoSchema(many=True)

@app.route('/videos', methods=['POST'])
def create_video():

    title = request.json['title']
    description = request.json['description']
    
    new_video = videos(title, description)
    db.session.add(new_video)
    db.session.commit()

    return video_schema.jsonify(new_video)

@app.route('/videos', methods=['GET'])
def get_videos():
    all_videos = videos.query.all()
    result = videos_schema.dump(all_videos)
    return jsonify(result)

@app.route('/videos/<id>', methods=['GET'])
def get_video(id):
    video = videos.query.get(id)
    return video_schema.jsonify(video)

@app.route('/videos/<id>', methods=['PUT'])
def update_video(id):
    video = videos.query.get(id)

    title = request.json['title']
    description = request.json['description']

    video.title = title
    video.description = description

    db.session.commit()
    return video_schema.jsonify(video)

@app.route('/videos/<id>', methods=['DELETE'])
def delete_task(id):
    video = videos.query.get(id)
    db.session.delete(video)
    db.session.commit()

    return video_schema.jsonify(video)


if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()


