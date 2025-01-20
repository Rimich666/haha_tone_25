from flask import Flask, request

from make_response.make_response import make_response

app = Flask(__name__)


@app.route('/alice', methods=['POST'])
def resp():
    req = request.json.get('request', {})
    return make_response(
        req.get('nlu').get('intents'),
        request.json.get('state').get('session'),
        req.get('payload'),
        request.json.get('session'),
        req.get('nlu').get('tokens'),
        req.get('original_utterance')
    )


@app.route('/', methods=['GET'])
def get_response():
    return 'kjhngbkjnhgjkl'


app.run(host='0.0.0.0', port=5000, debug=True)
