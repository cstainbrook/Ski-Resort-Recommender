from flask import Flask, render_template, request, url_for, redirect
import datetime
import graphlab as gl
import pandas as pd

app = Flask(__name__)

def make_resort_list(resorts):
    resort_list = []
    for resort in resorts['Resort Name'].values:
        resort_list.append(resort)
    return resort_list

@app.route('/', methods=['GET', 'POST'])
def index():
    resort_name_list = make_resort_list(resorts)
    error1 = error2 = None
    if request.method == "POST":
        user = request.form['user_id']
        return redirect(url_for('recommender', user_id=user))
    return render_template('index.html', resort_name_list=resort_name_list)

@app.route('/<user_id>')
def recommender(user_id):
    recs = model.recommend([user_id])['Resort Name']
    return render_template('recommender.html', recommendations=recs)

@app.route('/<resort_name>')
def new_user_recommender(resort_name):
    new_sf = gl.SFrame({'Resort Name':[resort_name]})
    recs = model.recommend_from_interactions(new_sf)['Resort Name']
    return render_template('recommender_new_user.html', recommendations=recs)

if __name__ == '__main__':
    model = gl.load_model('../models/factorization_model')
    resorts = pd.read_csv('../resort_names.csv')
    app.run(host='0.0.0.0', port=7012, debug=True, threaded=True)
