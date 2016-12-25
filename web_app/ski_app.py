from flask import Flask, render_template, request, url_for, redirect
import datetime
import graphlab as gl

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    error1 = error2 = None
    if request.method == "POST":
        user = request.form['user_id']
        return redirect(url_for('recommender', user_id=user))
    return render_template('index.html')

@app.route('/<user_id>')
def recommender(user_id):
    recs = model.recommend([user_id])['Resort Name']
    return render_template('recommender.html', recommendations=recs)

if __name__ == '__main__':
    model = gl.load_model('../models/factorization_model')
    app.run(host='0.0.0.0', port=7011, debug=False, threaded=True)
