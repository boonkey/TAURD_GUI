from flask import Flask,render_template, request, jsonify
from common import *
import json, logging

app = Flask(__name__)

class WebInterface:
    def __init__(self, _verbose=False):
        self.info = "dan"
        if not _verbose:
            log = logging.getLogger('werkzeug')
            log.setLevel(logging.ERROR)
        else:
            print_message('WebInterface starting in verbose mode','info')

    @app.route("/")
    def main_page(self = None):
        if len(request.args) == 0:
            print_message('Browser page has been open', 'info')
            page = load_page("gui/index.html")
            return page
        elif 'task' in request.args:    
                if request.args.get('task') == 'get_info':
                    print_message('Browser - Getting sensors metadata', 'info')
                    with open('tmp_info','r') as f:
                        data="".join(f.readlines())
                    return jsonify(data)
                elif request.args.get('task') == 'get_data':
                    # Browser - sending sensors value
                    try:
                        with open('tmp','r') as f:
                            data="".join(f.readlines())
                        return jsonify(data)
                    except IOError, e:
                        if e.errno != 2:
                            raise
                        print_message('WebInterface - tmp file not found', 'warn')
        # Browser - saving sensors value
        # print_message('Browser - saving sensors value', 'info')
        sensor_data = json.dumps(request.args)
        with open('tmp','w') as f:
            f.write(sensor_data)
        return sensor_data

    def run(self, guireceiver):
        if guireceiver is None:
            raise NotImplementedError
        print_message('Site is Starting', 'info')
        app.run(port=8000, host="127.0.0.1")
