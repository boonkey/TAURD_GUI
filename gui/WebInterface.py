from flask import Flask,render_template, request, jsonify
import os, json
app = Flask(__name__)

global sensor_data

def load_page(localpath):
    with open(localpath,'rb') as indexfile:
        data = indexfile.readlines()
    #print data
    return "".join(data)

class WebInterface:
    def __init__(self):
        self.info = "dan"

    @app.route("/")
    def main_page(self = None):
        if len(request.args) == 0:
            print "this is the end"
            page = load_page("gui/index.html")
            return page
        elif 'task' in request.args:    
                if request.args.get('task') == 0:
                    #return all sensors metadata
                    i=0
                else:
                    #return sensors data
                    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    with open('tmp','r') as f:
                        data="".join(f.readlines())
                        print data
                    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    return jsonify(data)
        sensor_data = json.dumps(request.args)
        with open('tmp','w') as f:
            f.write(sensor_data)
        return sensor_data

    def run(self, guireceiver):
        if guireceiver == None:
            raise NotImplementedError
        app.run(port=8000, host="127.0.0.1")
