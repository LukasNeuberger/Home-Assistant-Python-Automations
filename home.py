import os
import asyncio
import websockets
import json
import custom_logging
import time

homeassistant_domain = os.environ['HOMEASSISTANT_DOMAIN']
api_access_token = os.environ['HOMEASSISTANT_API_TOKEN']

debug = False
if "DEBUG" in os.environ and os.environ["DEBUG"] == "True":
    debug = True

state = {}
state_changed_callbacks = set()
event_callbacks = set()
state_initialized_callbacks = set()
websocket = None
next_id = 1


def get_state():
    return state


def register_state_changed_callback(fct):
    state_changed_callbacks.add(fct)


def remove_state_changed_callback(fct):
    state_changed_callbacks.discard(fct)


def trigger_state_changed(entity, new_state, old_state):
    for f in state_changed_callbacks:
        try:
            f(entity, new_state, old_state)
        except Exception as ex:
            custom_logging.log(__name__, "Error while calling StateChanged callback %s: %s %s" % (str(f), type(ex), str(ex)))


def register_event_callback(fct):
    event_callbacks.add(fct)


def remove_event_callback(fct):
    event_callbacks.discard(fct)


def trigger_event(entity, data):
    for f in event_callbacks:
        try:
            f(entity, data)
        except Exception as ex:
            custom_logging.log(__name__, "Error while calling Event callback %s: %s %s" % (str(f), type(ex), str(ex)))


def register_state_initialized_callback(fct):
    state_initialized_callbacks.add(fct)


def remove_state_initialized_callback(fct):
    state_initialized_callbacks.discard(fct)


def trigger_state_initialized():
    for f in state_initialized_callbacks:
        try:
            f(state)
        except Exception as ex:
            custom_logging.log(__name__, "Error while calling StateInitialized callback %s: %s %s" % (str(f), type(ex), str(ex)))


def send_command(domain, service, service_data={}):
    global next_id
    msg = json.dumps(
        {
            "id": next_id,
        "type": "call_service",
        "domain": domain,
        "service": service,
        "service_data": service_data
    }
    )
    next_id += 1

    if (debug):
        custom_logging.log(__name__, "Sending message: %s" % msg)
    asyncio.get_event_loop().create_task(websocket.send(msg))


async def main():
    global websocket
    global next_id
    while True:
        try:
            websocket = await websockets.connect('ws://%s/api/websocket' % homeassistant_domain)
            custom_logging.log(__name__, "Connected to %r" % str(websocket.remote_address))

            msg = {'type': 'auth', 'access_token': api_access_token}
            if (debug):
                custom_logging.log(__name__, "Sending message: %s" % msg)
            await websocket.send(json.dumps(msg))

            get_state_msg_id = next_id
            msg = {'id': get_state_msg_id, "type": "get_states"}
            next_id += 1
            if (debug):
                custom_logging.log(__name__, "Sending message: %s" % msg)
            await websocket.send(json.dumps(msg))

            state_initialized = False
            while not state_initialized:
                message = await websocket.recv()

                if message is None:
                    break
                dic = json.loads(message)

                # if debug output is activated via DEBUG environment variable, print received payload
                if (debug):
                    custom_logging.log(__name__, "Receiving message while initializing: %s" % dic)

                # initialize state with result of initial get_state request and trigger callbacks of apps
                if (dic["type"] == "result" and dic["id"] == get_state_msg_id):
                    get_state_msg_id = None
                    for el in dic["result"]:
                        entity = el["entity_id"]
                        state[entity] = el
                    trigger_state_initialized()
                    state_initialized = True

            msg = {'id': next_id, 'type': 'subscribe_events', 'event_type': 'state_changed'}
            next_id += 1
            if (debug):
                custom_logging.log(__name__, "Sending message: %s" % msg)
            await websocket.send(json.dumps(msg))

            msg = {'id': next_id, 'type': 'subscribe_events', 'event_type': 'deconz_event'}
            next_id += 1
            if (debug):
                custom_logging.log(__name__, "Sending message: %s" % msg)
            await websocket.send(json.dumps(msg))

            while True:
                message = await websocket.recv()

                if message is None:
                    break
                dic = json.loads(message)

                # if debug output is activated via DEBUG environment variable, print received payload
                if (debug):
                    custom_logging.log(__name__, "Receiving message: %s" % dic)

                # if the state of an entity has changed update state and trigger callbacks of apps
                if (dic["type"] == "event"):
                    if (dic["event"]["event_type"] == "state_changed"):
                        entity = dic["event"]["data"]["entity_id"]
                        new_state = dic["event"]["data"]["new_state"]
                        old_state = None

                        # get old state if it exists
                        if entity in state:
                            old_state = state[entity]

                        # update state
                        state[entity] = new_state

                        # trigger state changed callbacks
                        if ((old_state == None) or (state[entity] != old_state)):
                            trigger_state_changed(entity, new_state, old_state)

                    elif (dic["event"]["event_type"] == "deconz_event"):
                        entity = dic["event"]["data"]["id"]
                        data = dic["event"]["data"]["event"]
                        trigger_event(entity, data)
        except Exception as ex:
            custom_logging.log(__name__, "Websocket error: %s %s" % (type(ex), str(ex)))
            time.sleep(10)


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
