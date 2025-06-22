
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(20))
    genre = db.Column(db.String(50))
    notes = db.Column(db.String(200))

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    song_order = db.Column(db.String(500))

@app.route('/')
def index():
    shows = Show.query.all()
    return render_template('index.html', shows=shows)

@app.route('/create_show', methods=['GET', 'POST'])
def create_show():
    if request.method == 'POST':
        name = request.form['name']
        song_ids = request.form.getlist('songs')
        song_order = ','.join(song_ids)
        new_show = Show(name=name, song_order=song_order)
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        songs = Song.query.all()
        return render_template('create_show.html', songs=songs)

@app.route('/show/<int:show_id>')
def show_detail(show_id):
    show = Show.query.get_or_404(show_id)
    song_ids = [int(sid) for sid in show.song_order.split(',') if sid]
    songs = [Song.query.get(sid) for sid in song_ids]
    return render_template('show_detail.html', show=show, songs=songs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
