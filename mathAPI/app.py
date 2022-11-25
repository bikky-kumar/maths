from flask import Flask, request, jsonify, send_file

import os


# init app

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/min', methods=['GET'])
def min():
    numbers = request.json['numbers']
    min_number = numbers[0]
    for i in range(0, len(numbers)):
        if numbers[i] < min_number:
            min_number = numbers[i]
    return jsonify({'minimum_number': min_number})


@app.route('/max', methods=['GET'])
def max():
    numbers = request.json['numbers']
    max_number = numbers[0]
    for i in range(0, len(numbers)):
        if numbers[i] > max_number:
            max_number = numbers[i]
    return jsonify({'maximum_number': max_number})


@app.route('/avg', methods=['GET'])
def avg():
    numbers = request.json['numbers']
    avg = sum(numbers)/len(numbers)
    return jsonify({'average': avg})


@app.route('/median', methods=['GET'])
def median():
    numbers = sorted(request.json['numbers'])
    size = len(numbers)
    median = 0
    if size % 2 == 0:
        mid_point = int(size/2)-1
        median = (numbers[mid_point]+numbers[mid_point+1])/2
    else:
        mid_point = int((size/2)+0.5)-1
        print(mid_point)
        median = numbers[mid_point]
    return jsonify({'median': median})


# https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method
@app.route('/percentile', methods=['GET'])
def percentile():
    numbers = sorted(request.json['numbers'])
    P = request.json['quantifier']
    N = len(numbers)
    ordinal_rank = round(((P/100)*N)-1)
    return jsonify({'{}% Percentile'.format(P): numbers[ordinal_rank]})


@app.route('/ping', methods=['GET'])
def ping():
    file_name = basedir+"/tmp/ok.txt"
    print("/ping request: " + str(os.path.isfile(file_name)))
    if os.path.isfile(file_name):
        return "OK", 200
    else:
        return file_name, 503


@app.route('/img', methods=['GET'])
def img():
    file_name = basedir+"/tmp/giphy.gif"
    log_file = basedir+"/log/log.txt"
    print(os.path.isfile(file_name))
    try:
        f = open(log_file, "a")
        f.write(str({'ip': request.remote_addr, "request": str(request)}))
        f.close()
    except:
        print("cannot log the files")
    
    if os.path.isfile(file_name):
        return send_file(file_name, mimetype='image/gif')


# run server
if __name__ == '__main__':
    app.run(debug=True, port=3001)
