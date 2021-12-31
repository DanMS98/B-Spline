import os.path
from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from Spline import create_figure
import numpy as np
from flask_bootstrap import Bootstrap

"""
CREATIGN FLASK APP
"""
app = Flask(__name__)
Bootstrap(app)
UPLOAD_FOLDER = './static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "DANAXA"
db = SQLAlchemy(app)

"""
CREATING DEMO T, C AND K
"""
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
    """
    :return: None
    this is the main page of the web app. Based on the methods that were called, it returns
    a html page to browser. If the method is GET, it simply renders default page, if the method is post,
    it gets the params from the form and calls create_figure to create a spline on the uploaded image.
    if no params were entered as t, c and k, it uses default values which were initialed above.
    """

    if request.method == "GET":
        return render_template('index.html', name='new_plot', url='./static/images/corn.png')

    elif request.method == "POST":
        if 'file' not in request.files:
            flash('Picture not found')
            return redirect('/')

        file = request.files['file']
        T = request.form.get('T')
        C = request.form.get('C')
        K = request.form.get('K')

        print("t is ", t)
        if C is '':
            flash('no value for C declared, using default values')
            C = demo_ctr
        else:
            C = np.fromstring(C, dtype=float, sep=',')
            C = np.reshape(C, (-1, 2))
            print("C is ", C)

        if T is '':
            flash('no value for T declared, using default values')
            T = t
        else:
            T = np.fromstring(T, dtype=float, sep=',')
            print("T is ", T)

        if K is '':
            flash('no value for K declared, using default values')
            K = 3
        else:
            K = int(K)

        if file.filename == '':
            flash('No file selected')
            return redirect('/')

        if file and allowed_exts(file.filename):
            print(f'FILE NAME:{file.filename}')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            flash('image uploaded!')
            uploadedImageUrl = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print("FILENAME:", file.filename)
            figurePath = create_figure(T, C, K, uploadedImageUrl, file.filename)
            return render_template('index.html', name='new_plot', url=str(figurePath))


if __name__ == "__main__":
    app.run(debug=False)
