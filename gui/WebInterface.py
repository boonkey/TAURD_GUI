from flask import Flask,render_template, request, g
import os
app = Flask(__name__)


def load_page(localpath):
    with open(localpath,'rb') as indexfile:
        data = indexfile.readlines()
    #print data
    return "".join(data)


@app.route("/")
def main_page():
    if len(request.args) == 0:
        print os.getcwd()
        return load_page("gui/index.html")
    for item in request.args:
        print item, " = ", request.args.get(item)
    return "Fuck you"

def run(guireceiver):
    if guireceiver == None:
        raise NotImplementedError
    app.run(port=8000, host="127.0.0.1")

if __name__ == '__main__':
    run(None)