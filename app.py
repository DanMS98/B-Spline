import os.path

from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from Spline import create_figure
import numpy as np
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
UPLOAD_FOLDER = './static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "DANAXA"
db = SQLAlchemy(app)

demo_ctr = np.array([(232, 125), (315, 191), (326, 232), (278, 236), (203, 207), (182.3, 235.), (190, 250),
                    (172.5, 368), (85, 381), (0, 420), ])
t = np.linspace(0, 1, len(demo_ctr)-2, endpoint=True)
t = np.append([0, 0, 0], t)
t = np.append(t, [1, 1, 1])
k = 3

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_exts(filename):
    return '.' in filename and filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "GET":
        return render_template('index.html', name='new_plot', url='./static/images/kn2c.jpeg')

    elif request.method == "POST":
        if 'file' not in request.files:
            flash('File not found')
            return redirect('/')

        file = request.files['file']
        if file.filename == '':
            flash('Not File selected')
            return redirect('/')

        if file and allowed_exts(file.filename):
            print(f'FILE NAME:{file.filename}')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash('image uploaded!')
            uploadedImageUrl = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print("FILENAME:", file.filename)
            figurePath = create_figure(t, demo_ctr, k, uploadedImageUrl, file.filename)
            return render_template('index.html', name='new_plot', url=str(figurePath))


if __name__ == "__main__":
    app.run(debug=True)
