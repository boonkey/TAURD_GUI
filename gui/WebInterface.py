from flask import Flask,render_template, request, jsonify
from common import *
import os, json, logging

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


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
                if request.args.get('task') == 'get_info':
                    #return all sensors metadata
                    with open('tmp_info','r') as f:
                        data="".join(f.readlines())
                    return jsonify(data)
                elif request.args.get('task') == 'get_data':
                    #return sensors data
                    with open('tmp','r') as f:
                        data="".join(f.readlines())
                    return jsonify(data)
        sensor_data = json.dumps(request.args)
        with open('tmp','w') as f:
            f.write(sensor_data)
        return sensor_data

    def run(self, guireceiver):
        if guireceiver == None:
            raise NotImplementedError
        app.run(port=8000, host="127.0.0.1")
