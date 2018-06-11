#!/usr/bin/env python
"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
"""
@author Amit Agarwal
"""
"""
This script launches the middleware application.
"""
import socket

from flask import Flask, jsonify
from flask_cors import CORS

import dnac_c as dnac

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return jsonify({'message': 'hello world'})
# end

# get inventory from DNAC using serial
@app.route('/info_dnac/<serial>')
def get_info_serial(serial):
    data = dnac.get_device_by_serial(serial)
    if len(data):
        return data
    else:
        return jsonify()
# end

if __name__ == '__main__':
    app.run(debug=True, host=socket.gethostbyname(socket.gethostname()), port=7001)
# end
