from flask import Flask, request, jsonify

from api.results import *
from api.database import Database

app = Flask(__name__)

@app.route('/nlb', methods = ['POST'])
def nlb_result() :
    return NLBResults(request.form).get_result()

@app.route('/dlb', methods = ['POST'])
def dlb_result() :
    return DLBResults(request.form).get_result()

@app.route('/results', methods = ['GET'])
def get_results() :
    year = int(request.args['year'])
    month = int(request.args['month'])
    day = int(request.args['day'])

    result = Database().get_results(year, month, day)
    
    return result

def start() :
    app.run(host='0.0.0.0', port=5000, debug = True)