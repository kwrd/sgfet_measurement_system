import time
from pybleno import *
import sys
from receiver_characteristic import *

import datetime

def main():
    filepath = "/tmp/ble_{}.log".format(datetime.datetime.now().strftime('%Y-%m-%d'))
    with open(filepath, mode='w') as log:
        bleno = Bleno()
        
        def onStateChange(state):
            log.write('on -> stateChange: ' + state);
            if (state == 'poweredOn'):
                bleno.startAdvertising('receiver', ['ec00'])
            else:
                bleno.stopAdvertising();
              
        bleno.on('stateChange', onStateChange)

        def onAdvertisingStart(error):
            log.write('on -> advertisingStart: ' + ('error ' + error if error else 'success'));
            if not error:
                bleno.setServices([
                    BlenoPrimaryService({
                        'uuid': 'ec00',
                        'characteristics': [ 
                            ReceiverCharacteristic('ec0f')
                            ]
                    })
                ])
        bleno.on('advertisingStart', onAdvertisingStart)

        bleno.start()

        log.write('Hit <ENTER> to disconnect')

        if (sys.version_info > (3, 0)):
            input()
        else:
            raw_input()
        bleno.stopAdvertising()
        bleno.disconnect()
    print ('terminated.')
    sys.exit(1)

def onStateChange(state):
    if (state == 'poweredOn'):
        bleno.startAdvertising('receiver', ['ec00'])
    else:
        bleno.stopAdvertising();

def onStateChangeCallBack(log):
    log.write('on -> stateChange: ' + state);
    return onStateChange

if __name__ == '__main__':
    main()