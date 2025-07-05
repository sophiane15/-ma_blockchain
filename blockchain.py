from flask import Flask, jsonify, request
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine_block():
    last_block = blockchain.chain[-1]
    new_block = Block(len(blockchain.chain), last_block.hash, ["Nouvelle transaction"])
    blockchain.add_block(new_block)
    return jsonify({"message": "Bloc miné avec succès !", "hash": new_block.hash})

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({"longueur": len(blockchain.chain), "chaîne": [block.__dict__ for block in blockchain.chain]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
