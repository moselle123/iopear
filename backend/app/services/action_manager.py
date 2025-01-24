from datetime import datetime, timezone
import RPi.GPIO as GPIO
import logging
from app.models import Action
from app.models import Notification
from app.models import Actuator

class ActionManager():
	_actions = {}
	_actuators = {}

	@classmethod
	def initialise(cls):
		cls.update_action_list()
		cls.update_actuator_list()

	@classmethod
	def trigger_action(cls, action_id):
		action = cls._actions[action_id]
		if not action:
			logging.error(f"Action with ID {action_id} not found.")
			return

		actuator = cls._actuators.get(action["actuator_id"])
		if not actuator:
			logging.error(f"Actuator with ID {action['actuator_id']} not found.")
			return

		state = GPIO.HIGH if action["actuator_state"] else GPIO.LOW

		try:
			GPIO.output(actuator["pin"], state)

			now =  datetime.now(timezone.utc)
			Action.update(action_id, {"last_triggered": now})
			Notification.create("action", action_id, action["actuator_state"], now)

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
				"pin": actuator["pin"],
			}

			GPIO.setup(actuator["pin"], GPIO.OUT)
