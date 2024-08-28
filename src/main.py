import logging

from flask import Flask
from flask import url_for
from flask import request
from flask import render_template
from flask import redirect
from flask import jsonify

from dbwrapper import Connection, Local
from connectionData import connectionData
import translator

logging.basicConfig(level=logging.DEBUG)

import os

HOST = '127.0.0.1'
PORT = 8089
DEBUG=True

db_host = 'Penguin' if DEBUG else HOST
localDB = Local()
cd = connectionData()

app = Flask(
    import_name='DBTranslator',
    static_folder=f'{os.getcwd()}/static/',
    template_folder=f'{os.getcwd()}/templates/',
    )

print(os.getcwd() + '/static/')


@app.route('/dbt', methods=['POST', 'GET'])
def dbt():
    print(request.method)
    if request.method == 'GET':
        return render_template('login.html', error='')
    
    elif request.method == 'POST':
        print(request)
        database = request.form.get('database', None)
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        logging.debug(f'{database=}, {username=}, {password=}')
        
        if not database or not username or not password:
            return render_template('login.html', error='Please fill in all fields.')
        

        try:
            db = Connection(
                host=db_host, 
                username=username, 
                password=password, 
                database=database)
            
            db.connect()
            cd.host = db_host
            cd.username = username
            cd.password = password
            cd.database = database
            return render_template('configuration.html', version=db.db_version)

        except Exception as e:
            return render_template('login.html', error='Invalid credentials.')


@app.route('/copy', methods=['POST'])
def copyAndProcess():
    db = Connection(
        host=cd.host, 
        username=cd.username, 
        password=cd.password, 
        database=cd.database
    )
    db.connect()
    localDB = Local()
    localDB.dropAndCreateTable()

    mode = request.form.getlist('mode')

    if len(mode) > 0:
        mode = mode[0]
        logging.debug(mode)
    
    else:
        mode = 'all'

    if mode == 'noTranslation':
        prods = db.getEmptyProducts().fetchall()
        
    elif mode == 'sameTranslation':
        prods = db.getProductsWithSameTranslation().fetchall()

    else:
        prods = db.getProductData().fetchall()

    for prod in prods:
        localDB.addProduct(prod[0], prod[1], prod[2])

    return render_template('process.html')


@app.route('/process', methods=['POST'])
def process():
    return render_template('process.html')

@app.route('/api/getAllProducts', methods=['GET'])
def getAllProducts():
    data = localDB.getProductData().fetchall()
    return jsonify(data)
    
@app.route('/api/translate', methods=['GET'])
def translate():
    text = request.args.get('text')
    return jsonify(translator.translate(text))


@app.route('/api/getProduct', methods=['GET'])
def getExactProduct():
    barcode = request.args.get('barcode')
    data = localDB.getExactProduct(barcode)
    return jsonify(data)


@app.route('/api/updateName', methods=['GET'])
def updateName():
    code = request.args.get('barcode')
    name = request.args.get('name')
    localDB.updateName(code, name)


@app.route('/api/updateTranslation', methods=['GET'])
def updateTranslation():
    code = request.args.get('barcode')
    translation = request.args.get('translation')
    localDB.updateTranslation(code, translation)


app.run(host=HOST, port=PORT, debug=DEBUG, threaded=True)
