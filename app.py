from flask import Flask, render_template, session, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
import random

app = Flask(__name__)
app.secret_key = 'super secret key'

class OefeningenForm(FlaskForm):
    antwoord = IntegerField('name', validators=[DataRequired()], render_kw={'autofocus': True, 'autocomplete': "off"})

def MaakSommen(aantal=10, niveau=1):
    list=[]
    if niveau == 1:
        #van 0 tot 10

        for i in range(0,aantal):
            sum = random.randint(2,10)
            print sum
            eerste = random.randint(1,(sum-1))
            tweede = sum - eerste

            text = str(eerste)+" + "+str(tweede)+" = "
            list.append({"text":text, "result":sum})

    random.shuffle(list)
    return list

@app.route('/home')
def home():
    if 'count' in session:
        session.pop('count')
    return "hoi hoi "

@app.route('/sommen', methods=['GET', 'POST'])
def sommen():
    if request.method == 'GET':
        form = OefeningenForm()
        if not 'count' in session:
            session['count'] = 0
            session['oefeningen']=MaakSommen()
        oefening=session['oefeningen'][session['count']]
        return render_template('index.html', oefening=oefening, form=form, count=session['count'])
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
        return redirect(url_for('sommen'))

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
