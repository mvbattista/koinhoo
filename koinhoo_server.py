from flask import Flask, jsonify, request
from koinhoo import Koinhoo

app = Flask(__name__)


@app.route('/api/v1/rates', methods=['GET'])
def rates():
    by_rates = request.args.get('by_rates')
    kh = Koinhoo()
    return jsonify(kh.get_all_rates(by_rates=bool(by_rates)))


if __name__ == '__main__':
    app.run()
