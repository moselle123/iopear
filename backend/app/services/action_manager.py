from datetime import datetime, timezone
import RPi.GPIO as GPIO
import logging
from app.models import Action
from app.models import Notification
from app.models import Actuator

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ActionManager():
	_actions = {}
	_actuators = {}
	_app = None

	@classmethod
	def initialise(cls, app):
		cls.update_action_list()
		cls.update_actuator_list()
		cls._app = app

	@classmethod
	def trigger_action(cls, action_id):
		action = cls._actions[action_id]
		if not action:
			logger.error(f"Action with ID {action_id} not found.")
			return

		actuator = cls._actuators.get(action["actuator_id"])
		if not actuator:
			logger.error(f"Actuator with ID {action['actuator_id']} not found.")
			return

		state = GPIO.HIGH if action["actuator_state"] else GPIO.LOW

		try:
			GPIO.output(actuator["pin"], state)
			actuator["state"] = state

			now =  datetime.now(timezone.utc)
			with cls._app.app_context():
				Action.update(action_id, {"last_triggered": now})
				Notification.create("action", action_id, now)

				cls._app.config['SOCKET_IO'].emit('actuator-update', {
					"actuator_id": action["actuator_id"],
					"state": action["actuator_state"]
				})

				cls._app.config['SOCKET_IO'].emit('notification-update')

		except Exception as e:
			logging.error(f"Error triggering action: {e}")

	@classmethod
	def update_action_list(cls):
		actions = Action.get_actions()
		for action in actions:
			cls._actions[str(action["_id"])] = {
				"actuator_id": str(action["actuator_id"]),
				"actuator_state": action["actuator_state"],
				"duration": action.get("duration"),
			}

	@classmethod
	def update_actuator_list(cls):
		actuators = Actuator.get_actuators()
		for actuator in actuators:
			cls._actuators[str(actuator["_id"])] = {
				"name": actuator["name"],
				"pin": actuator["pin"],
				"state": False,
			}

			GPIO.setup(actuator["pin"], GPIO.OUT)

	@classmethod
	def get_actuators(cls):
		actuators = []
		for id, obj in cls._actuators.items():
			actuator = {
				"_id": str(id),
				"name": obj["name"],
				"pin": obj["pin"],
				"state": obj["state"],
			}
			actuators.append(actuator)

		return actuators
