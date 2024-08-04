##pub.py
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
from wifi import Red
Red("Familia Juchani","8884992sc")
rl_1=machine.Pin(2,machine.Pin.OUT)
mqtt_server = 'broker.emqx.io'
client_id = ubinascii.hexlify(machine.unique_id())
print(client_id)
topic_sub = b'Relay'
topic_sub1 = b'upd'
topic_pub = b'sensorqw'

last_message = 0
message_interval = 5
counter = 0

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'Relay':
        print(int(msg))
    if topic == b'upd':
        if(int(msg)>1):
            import upd
        print(bool(msg))

def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    client.subscribe(topic_sub1)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(1)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'{}'.format(counter)
      client.publish(topic_pub, msg)
      client.publish(b'estado', b'{}'.format(rl_1.value()))
      last_message = time.time()
      counter += 1
      rl_1.value(not rl_1.value())
  except OSError as e:
    restart_and_reconnect()