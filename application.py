from flask import Flask, jsonify,render_template, request, make_response,redirect
import cryptograms
import json
import random

# create our little application :)
application = Flask(__name__)


@application.route('/', methods=['GET'])
def main():
    gameId = random.sample(range(0,1000),1)[0]
    return redirect('/game/'+str(gameId))


@application.route('/game/<gameId>', methods=['GET'])
def genGame(gameId):

    gameIdInt = int(gameId)
    datafilePath = 'static/data/quotes.csv'
    original, author = cryptograms.loadData(gameIdInt, datafilePath)

    keyMap = cryptograms.genKeys(original, difficulty = 3)
    encrypted = cryptograms.encrypt(original, keyMap)
    userKeys = cryptograms.getUserKeys(keyMap)

    resp = make_response(render_template('index.html',
            encrypted= encrypted, author =author, userKeys = userKeys))

    resp.set_cookie('encrypted', json.dumps(encrypted))
    resp.set_cookie('author', json.dumps(author))
    resp.set_cookie('userKeys', json.dumps(userKeys))

    return resp

@application.route('/game/<gameId>', methods=['POST'])
def scoreAnswer(gameId):

    encrypted = json.loads(request.cookies.get('encrypted'))
    author = json.loads(request.cookies.get('author'))
    userKeys = json.loads(request.cookies.get('userKeys'))

    userInputs={}
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            if value!='':
                userInputs[key] = value

    result= cryptograms.encrypt(encrypted,userInputs)
    scoreText = cryptograms.score(userInputs,userKeys)

    resp = make_response(render_template('index.html',
            encrypted=encrypted, author=author, userKeys=userKeys, scoreText= scoreText, result = result))
    return resp

if __name__ == "__main__":
    application.run()