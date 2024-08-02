##pub.py
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
from wifi import Red
Red("Familia Juchani","8884992sc")

mqtt_server = 'broker.emqx.io'
client_id = ubinascii.hexlify(machine.unique_id())
print(client_id)
topic_sub = b'notification'
topic_sub1 = b'upd'
topic_pub = b'sensorqw'

last_message = 0
message_interval = 1
counter = 0

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification':
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
    time.sleep(10)
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
      last_message = time.time()
      counter += 1
  except OSError as e:
    restart_and_reconnect()