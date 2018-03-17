from flask import Flask,render_template, request
import os
app = Flask(__name__)

def load_page(localpath):
    with open(localpath,'rb') as indexfile:
        data = indexfile.readlines()
    print data
    return "".join(data)


@app.route("/")
def main_page():
    if len(request.args) == 0:
        print os.getcwd()
        return load_page("gui/index.html")
    return "Fuck you"

def run():
    app.run(port=8000, host="127.0.0.1")

if __name__ == '__main__':
    run()