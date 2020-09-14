from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# using pgadmin psql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:yourpassword@localhost/quotes'
#to deploy using heroku
#app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://rqaxnukzqkwqax:bede3b5c46b7fc2f134b386b56a99d2946ea3e1b2653a7c2827113327f8918fb@ec2-52-48-65-240.eu-west-1.compute.amazonaws.com:5432/d8fhdtg045n27t'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
dbb = SQLAlchemy(app)


class favquotes (dbb.Model):
    id = dbb.Column(dbb.Integer, primary_key=True)
    author = dbb.Column(dbb.String(30))
    quote = dbb.Column(dbb.String(500))


@app.route('/')
def index():
    result = favquotes.query.all()
    return render_template('index.html',result=result)




@app.route('/quotes')
def quotes():
    return render_template('quotes.html')


@app.route('/process', methods=['POST'])
def process():
    author = request.form['author']
    quote = request.form['quote']
    quotedata=favquotes(author=author,quote=quote)
    dbb.session.add(quotedata)
    dbb.session.commit()
    return redirect(url_for('index'))
    
