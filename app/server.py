from flask import Flask, request, jsonify
from .switchmate import get_peripheral, scan, switch, MANUFACTURER_DATA_AD_TYPE
import datetime, json

MAX_RETRIES = 5

app = Flask(__name__)

def get_error(*messages):
    return {"status": "error", "msg": '; '.join(messages)}

@app.route('/iot/switchmate', methods=['GET'])
def switchmate_get():
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
        process_entry=lambda switchmate: switchmates.append([
            switchmate.addr,
            ("off", "on")[int(switchmate.getValueText(MANUFACTURER_DATA_AD_TYPE)[1])],
        ]),
    )

    return jsonify(switchmates)

@app.route('/iot/switchmate/toggle', methods=['POST'])
def switchmate_toggle():
    print(str(datetime.datetime.now()) + ' - Toggling Switchmate...')
    req_data = request.get_json()
    mac_address = req_data.get('mac_address')
    val = b'\x01' if req_data.get('on') else (b'\x00' if req_data.get('off') else None)
    is_original = req_data.get('is_original')
    
    if not mac_address:
        return jsonify(get_error('mac_address is required'))

    device = get_peripheral(mac_address)

    # Retry to search for device
    if not device:
        retries = 0

        while not device and retries < MAX_RETRIES:
            retries += 1
            device = get_peripheral(mac_address)

    if device:
        try:
            switch(device, val, is_original)
        except Exception as ex:
            print(str(datetime.datetime.now()) + ' - ERROR: ' + ex.message)
            if 'disconnected' in ex.message.lower():
                return jsonify(get_error('Device disconnected.'))
            else:
                return jsonify(get_error(ex.message))
        return jsonify({"status": "done"})

    return jsonify(get_error('Device not found.'))

app.run(host='0.0.0.0', port=5000)