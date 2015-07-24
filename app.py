from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    # app.debug = True
    # listen on all public IPs
    # app.run(host='0.0.0.0')
    app.run()