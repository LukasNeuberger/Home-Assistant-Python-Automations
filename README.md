# Home-Assistant-Python-Automations

App-Damon was kind of a hassle, so I started my own Home Assistant Python Automation system.
startup.py is the entry point.
It first looks for python files in the subfolder './Automations' and calls function 'initialize' if it exists.
Here automations can intialize before a connection to the Home Assistant server is established and register callbacks for state changed events.
Then the connection to the Home Assistant server is established.
For this, Environment variables 'HOMEASSISTANT_DOMAIN' and 'HOMEASSISTANT_API_TOKEN' need to be configured.
Afterwards, the states of all entities are requested and stored, automations can access this through 'home.get_state()'
Then the scripts subscribes to 'state_changed' and 'deconz_event' events and triggers all registered callbacks when such a message is sent by Home Assistant.
