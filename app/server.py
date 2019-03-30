from flask import Flask, request, jsonify
from .switchmate import get_peripheral, scan, switch
import datetime, json

app = Flask(__name__)

def get_error(*messages):
    return {"status": "error", "msg": "' + '\n'.join(messages) + '"}

@app.route('/iot/switchmate', methods=['GET'])
def switchmate_scan():
    switchmates = []
    if request.args.get('timeout'):
        try:
            timeout = float(request.args.get('timeout'))
            if timeout <= 0:
                timeout = 1
        except ValueError:
            return jsonify(get_error('Timeout must be a integer or float.'))
    else:
        timeout = 1
        
    scan(
        str(datetime.datetime.now()) + ' - Scanning Switchmate...',
        timeout=timeout,
        process_entry=lambda switchmate: switchmates.append(switchmate.addr),
    )

    return jsonify(switchmates)

@app.route('/iot/switchmate/toggle', methods=['POST'])
def switchmate_toggle():
    print(str(datetime.datetime.now()) + ' - Toggling Switchmate...')
    req_data = request.get_json()
    mac_address = req_data['mac_address']
    if not mac_address:
        return jsonify(get_error('mac_address is required'))

    device = get_peripheral(mac_address)
    if device:
        try:
            switch(device, None)
        except Exception as ex:
            print(str(datetime.datetime.now()) + ' - ERROR: ' + ex.message)
            if 'disconnected' in ex.message.lower():
                return jsonify(get_error('Device disconnected.'))
            else:
                return jsonify(get_error(ex.message))
        return jsonify({"status": "done"})
    return jsonify(get_error('Device not found.'))

app.run(host='0.0.0.0', port=5000)