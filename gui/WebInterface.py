from flask import Flask,render_template, request
import os, json
app = Flask(__name__)

global sensor_data

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
    elif 'task' in request.args:    
            if request.args.get('task') == 0:
                #return all sensors metadata
                i=0
            else:
                #return sensors data
                return "damn"
    sensor_data = json.dumps(request.args)      
    return sensor_data

def run(guireceiver):
    if guireceiver == None:
        raise NotImplementedError
    app.run(port=8000, host="127.0.0.1")

if __name__ == '__main__':
    run(None)