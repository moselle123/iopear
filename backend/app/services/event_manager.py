from durable.lang import *
from datetime import datetime, timezone
from app.models import Event
from app.models import Notification
from .action_manager import ActionManager
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_events(measurement, value):
	events = Event.get_events(measurement=measurement, enabled=True)

	for event in events:
		last_triggered = event["last_triggered"]
		hours_off = 0
		if last_triggered:
			elapsed = datetime.now(timezone.utc) - last_triggered
			hours_off = elapsed.total_seconds() / 3600

		#post_fact(str(event["_id"]), {"measurement": measurement, "value": value, "hours_off": hours_off})

def load_rules(event_id=None):
	try:
		if event_id:
			event = Event.get_events(id=event_id)
			if event and event["is_enabled"]:
				events = [event]
			else:
				logger.error(f"Cannot load rules for this event with id {event_id}, it is either not found or not enabled.")
				return
		else:
			events = Event.get_events(enabled=True)

		for event in events:
			logger.info(f"Initializing ruleset for event ID: {event}")
			with ruleset("test"):
				condition = None
				for cond in event["conditions"]:
					logger.info(cond)
					if cond["type"] == "less_than":
						sub_condition = m.value < cond["value"]
					elif cond["type"] == "greater_than":
						sub_condition = m.value > cond["value"]
					elif cond["type"] == "time_elapsed":
						sub_condition = m.hours_off > cond["value"]

					if condition is None:
						condition = sub_condition
					else:
						condition = condition & sub_condition

				logic = all if event["logic"] == "AND" else any
				condition = logic([condition])

				@when_all(condition)
				def trigger_event(c):
					print(f"Event triggered")
					for action_id in event["actions"]:
						ActionManager.trigger_action(action_id)

					now = datetime.now(timezone.utc)
					Event.update(event_id, {"last_triggered": now})
					Notification.create(notification_type="event", entity_id=event["_id"], value=c.m.value, timestamp=now)

	except Exception as e:
		logger.error(f"Error loading rules: {e}")

def post_fact(ruleset_name, fact):
	try:
		logger.info(f"Posting fact to ruleset '{ruleset_name}': {fact}")
		post("test", fact)
	except Exception as e:
		logger.error(f"Error posting fact to ruleset '{ruleset_name}': {e}")
