from flask import Flask, render_template, session, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired
import random
from random import SystemRandom

app = Flask(__name__)
app.secret_key = 'super secret key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
#db = SQLAlchemy(app)

class OefeningenForm(FlaskForm):
    antwoord = IntegerField('name', validators=[DataRequired()], render_kw={'autofocus': True, 'autocomplete': "off", 'inputmode': "numeric"})

class HomeForm(FlaskForm):
    naam = StringField('Naam', render_kw={'autofocus': True, 'autocomplete': "off"})
    oefening = SelectField('Oefening', choices=[("optellen", "optellen"),("aftrekken","aftrekken")])
    niveau = SelectField('Niveau', choices=[(1,1),(2,2),(5,5)])
    submit = SubmitField('Start!')

def MaakSommen(aantal=10, niveau=1):
    list=[]
    if niveau == 1:
        #van 0 tot 10
        for i in range(0,aantal):
            sum = random.randint(2,10)
            eerste = random.randint(1,(sum-1))
            tweede = sum - eerste

            text = str(eerste)+" + "+str(tweede)+" = "
            list.append({"text":text, "result":sum})
    elif niveau == 2:
        # van 10 tot 20
        for i in range(0,aantal):
            sum = random.randint(10,20)
            eerste = random.randint(10,(sum-1))
            tweede = sum - eerste

            text = str(eerste)+" + "+str(tweede)+" = "
            list.append({"text":text, "result":sum})

    random.shuffle(list)
    return list

def MaakSplitsingen(aantal=10, niveau=5):
    list=[]
    if niveau == 1:
        #van 0 tot 10
        for i in range(0,aantal):
            eerste = random.randint(2,10)
            tweede = random.randint(1,(eerste-1))
            uitkomst = eerste - tweede

            text = str(eerste)+" - "+str(tweede)+" = "
            list.append({"text":text, "result":uitkomst})
    elif niveau == 2:
        # van 10 tot 20
        for i in range(0,aantal):
            eerste = random.randint(10,20)
            tweede = random.randint(10,(eerste-1))
            uitkomst = eerste - tweede

            text = str(eerste)+" - "+str(tweede)+" = "
            list.append({"text":text, "result":uitkomst})
    elif niveau == 5:
        # tot 1000, zonder bruggetje
        for i in range(0,100):
            eerste = random.randint(200,1000)
            print eerste
            tweede=""
            for j in str(eerste):
                print "j "+j
                max=int(j)
                tweede = tweede + str(random.randint(0,max))
                print "tw " +tweede

            tweede = int(tweede)
            uitkomst = eerste - tweede

            text = str(eerste)+" - "+str(tweede)+" = "
            list.append({"text":text, "result":uitkomst})
    random.shuffle(list)
    list=random.sample(list, aantal)
    return list

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if 'count' in session:
            session.pop('count')
        home_form=HomeForm()

        return render_template('index.html', home_form=home_form)

    if request.method == 'POST':
        session['naam'] = request.form['naam']
        session['oefening'] = request.form['oefening']
        session['niveau'] = request.form['niveau']

        return redirect(url_for('oefeningen'))


@app.route('/restart')
def restart():
    session.pop('count')
    return redirect(url_for('home'))

@app.route('/oefeningen', methods=['GET', 'POST'])
def oefeningen():
    if request.method == 'GET':
        form = OefeningenForm()
        if not 'count' in session:
            session['count'] = 0

            if session['oefening'] == 'optellen':
                session['oefeningen']=MaakSommen(niveau=session['niveau'])
            elif session['oefening'] == 'aftrekken':
                session['oefeningen']=MaakSplitsingen()

        oefening=session['oefeningen'][session['count']]
        return render_template('oefening.html', oefening=oefening, form=form, session=session)
    if request.method == 'POST':
        count = session['count']
        oefening = session['oefeningen'][count]
        oefening['antwoord'] = int(request.form['antwoord'])
        if int(request.form['antwoord']) == int(oefening['result']):
            oefening['score'] = 1
            print "ok"
        else:
            oefening['score'] = 0
            print "nok"
        #oefening['tijd'] = request.form['tijd']
        session['oefeningen'][count] = oefening
        session['count'] = session['count'] + 1

        if session['count'] >= 10:
            session.pop('count')
            return redirect(url_for('result'))
        return redirect(url_for('oefeningen'))

@app.route('/result')
def result():
    if 'count' in session:
        session.pop('count')
    score = 0
    for oef in session['oefeningen']:
        score = score + int(oef['score'])
    score = str(score) + "/" + str(len(session['oefeningen']))
    oefeningen = session['oefeningen']

    return render_template('result.html', oefeningen=oefeningen, score=score)

if __name__ == '__main__':
    app.run()
