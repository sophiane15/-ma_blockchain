from flask import Flask, jsonify
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({"blockchain": [block.__dict__ for block in blockchain.chain]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
