from pybleno import *
import sys
import signal
from receiver_characteristic import *

print('bleno - receiver');

bleno = Bleno()

def onStateChange(state):
   print('on -> stateChange: ' + state);

   if (state == 'poweredOn'):
     bleno.startAdvertising('receiver', ['ec00'])
   else:
     bleno.stopAdvertising();

bleno.on('stateChange', onStateChange)
    
def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

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

print ('Hit <ENTER> to disconnect')

if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

print ('terminated.')
sys.exit(1)
