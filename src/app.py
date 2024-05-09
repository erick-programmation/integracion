from flask import Flask, jsonify
from cashTransform import cash
from Products import products

app = Flask(__name__)

@app.route('/',methods=['GET'])
def ping():
    return jsonify({"response":"hello flask"})

@app.route('/products')
def productsHandler():
    return jsonify({"products":products})

@app.route('/cashtransform')
def cashHandler():
    return jsonify({"Cashtransform": products})

if __name__ == '__main__':
    app.run(host ="0.0.0.0", port=4000, debug=True)