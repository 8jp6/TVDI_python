from flask import Flask

app = Flask(__name__)

@app.route('/index')
def index():
    return '''
    <ul>
        <li>Hello, World!</li>
        <li>Hello, World!</li>
    </ul>
    '''

@app.route('/p1')
def hello_world():
    return '''
    <ul>
        <li>Hello, World!</li>
        <li>Hello, World!</li>
    </ul>
    '''