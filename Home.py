import asyncws
import json
import asyncio
import os

HomeassistantDomain = os.environ['HOMEASSISTANT_DOMAIN']
API_AccessToken = os.environ['HOMEASSISTANT_API_TOKEN']

Debug = False
if "DEBUG" in os.environ and os.environ["DEBUG"] == "True":
    Debug = True

state = {}
stateChangedCallbacks = set()
eventCallbacks = set()
stateInitializedCallbacks = set()
websocket = None
nextId = 1


def getState():
    return state


def registerStateChangedCallback(fct):
    stateChangedCallbacks.add(fct)


def removeStateChangedCallback(fct):
    stateChangedCallbacks.discard(fct)


def triggerStateChanged(entity, newState, oldState):
    for f in stateChangedCallbacks:
        f(entity, newState, oldState)


def registerEventCallback(fct):
    eventCallbacks.add(fct)


def removeEventCallback(fct):
    eventCallbacks.discard(fct)


def triggerEvent(entity, data):
    for f in eventCallbacks:
        f(entity, data)


def registerStateInitializedCallback(fct):
    stateInitializedCallbacks.add(fct)


def removeStateInitializedCallback(fct):
    stateInitializedCallbacks.discard(fct)


def triggerStateInitialized():
    for f in stateInitializedCallbacks:
        f(state)


def sendCommand(domain, service, service_data={}):
    global nextId
    msg = json.dumps(
        {
            "id": nextId,
            "type": "call_service",
            "domain": domain,
            "service": service,
            "service_data": service_data
        }
    )
    nextId += 1

    if(Debug):
        print("Sending message: %s" % msg)
    asyncio.get_event_loop().create_task(websocket.send(msg))


async def main():
    global websocket
    global nextId
    websocket = await asyncws.connect('ws://%s/api/websocket' % HomeassistantDomain)

    await websocket.send(json.dumps(
        {'type': 'auth',
         'access_token': API_AccessToken}
    ))

    getStateMsgId = nextId
    nextId += 1
    await websocket.send(json.dumps(
        {'id': getStateMsgId, "type": "get_states"}
    ))

    stateInitialized = False
    while not stateInitialized:
        message = await websocket.recv()

        if message is None:
            break
        dic = json.loads(message)

        # if debug output is activated via DEBUG environment variable, print received payload
        if(Debug):
            print(dic)

        # initialize state with result of initial getState request and trigger callbacks of apps
        if(dic["type"] == "result" and dic["id"] == getStateMsgId):
            getStateMsgId = None
            for el in dic["result"]:
                entity = el["entity_id"]
                state[entity] = el
            triggerStateInitialized()
            stateInitialized = True

    subscribeId = nextId
    nextId += 1
    await websocket.send(json.dumps(
        {'id': subscribeId, 'type': 'subscribe_events', 'event_type': 'state_changed'}
    ))

    subscribeId = nextId
    nextId += 1
    await websocket.send(json.dumps(
        {'id': subscribeId, 'type': 'subscribe_events', 'event_type': 'deconz_event'}
    ))

    while True:
        message = await websocket.recv()

        if message is None:
            break
        dic = json.loads(message)

        # if debug output is activated via DEBUG environment variable, print received payload
        if(Debug):
            print(dic)

        # if the state of an entity has changed update state and trigger callbacks of apps
        if(dic["type"] == "event"):
            if(dic["event"]["event_type"] == "state_changed"):
                entity = dic["event"]["data"]["entity_id"]
                newState = dic["event"]["data"]["new_state"]
                oldState = None

                # get old state if it exists
                if entity in state:
                    oldState = state[entity]

                # update state
                state[entity] = newState

                # trigger state changed callbacks
                if((oldState == None) or (state[entity] != oldState)):
                    triggerStateChanged(entity, newState, oldState)

            elif(dic["event"]["event_type"] == "deconz_event"):
                entity = dic["event"]["data"]["id"]
                data = dic["event"]["data"]["event"]
                triggerEvent(entity, data)


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
