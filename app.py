from flask import Flask, request

from make_response import make_response
# from repository.ydb_base import YdbBase
import repository.repository

# base = YdbBase()
app = Flask(__name__)


@app.route('/alice', methods=['POST'])
def resp():
    req = request.json.get('request', {})
    print(request.json)
    return make_response(
        req.get('nlu').get('intents'),
        request.json.get('state').get('session'),
        req.get('payload'),
        request.json.get('session').get('new'),
        req
    )


app.run(host='0.0.0.0', port=5000, debug=True)
