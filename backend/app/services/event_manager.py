from durable.lang import *
from datetime import datetime, timezone
from app.models import Event
from app.models import Notification
from .action_manager import ActionManager
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
from apscheduler.schedulers.background import BackgroundScheduler

class EventManager:
	_scheduler = BackgroundScheduler()
	_events = []

	@classmethod
	def update_event_list(cls, event_id=None):
		events = Event.get_events(id=event_id, enabled=True)

		for event in events:
			event["_id"] = str(event["_id"])
			for action_id in event["actions"]:
				action_id = str(action_id)
			cls._events.append(event)

			if event["scheduled_time"]:
				cls._schedule_event(event)
			if len(event["conditions"]):
				cls._load_rules(event)

	@classmethod
	def _schedule_event(cls, event):
		hour, minute = map(int, event["scheduled_time"].split(":"))
		def trigger_event():
			cls._trigger_event(event)

		cls._scheduler.add_job(trigger_event, 'cron', hour=hour, minute=minute, id=event["_id"])

	@classmethod
	def check_events(cls, measurement, value):
		for event in cls._events:
			if len(event["conditions"]):
				cls._post_fact(event["_id"], {"measurement": measurement, "value": value})

	@classmethod
	def _load_rules(cls, event):
		try:
			logger.info(f"Initializing ruleset for event ID: {event}")
			with ruleset(event["_id"]):
				condition = None
				for cond in event["conditions"]:
					if cond["measurement"] == m.measurement:
						if cond["type"] == "less_than":
							sub_condition = m.value < cond["value"]
						elif cond["type"] == "greater_than":
							sub_condition = m.value > cond["value"]

					condition = condition & sub_condition if condition else sub_condition

				logic = all if event["logic"] == "AND" else any
				condition = logic([condition])

				@when_all(condition)
				def trigger_event(c):
					cls._trigger_event(event, c.m.value)

		except Exception as e:
			logger.error(f"Error loading rules: {e}")

	@classmethod
	def _post_fact(ruleset_name, fact):
		try:
			logger.info(f"Posting fact to ruleset '{ruleset_name}': {fact}")
			post("test", fact)
		except Exception as e:
			logger.error(f"Error posting fact to ruleset '{ruleset_name}': {e}")

	@staticmethod
	def _trigger_event(event, value):
		for action_id in event["actions"]:
			ActionManager.trigger_action(action_id)

		now = datetime.now(timezone.utc)
		Event.update(event["_id"], {"last_triggered": now})
		Notification.create(notification_type="event", entity_id=event["_id"], value=value, timestamp=now)

	@classmethod
	def delete_event():
		pass
