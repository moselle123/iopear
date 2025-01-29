from datetime import datetime, timezone, timedelta
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
	_rulesets = []
	_latest_readings = None

	@classmethod
	def update_event_list(cls, event_id=None):
		events = Event.get_events(id=event_id, enabled=True)
		if event_id:
			events = [events]

		for event in events:
			event["_id"] = str(event["_id"])
			cls._events.append(event)

			if event["scheduled_time"]:
				cls._schedule_event(event)

	@classmethod
	def _schedule_event(cls, event):
		hour, minute = map(int, event["scheduled_time"].split(":"))
		def trigger_event():
			if len(event["conditions"]):
				cls._check_rules(event, cls._latest_readings, True)
			else:
				cls._trigger_event(event)

		cls._scheduler.add_job(trigger_event, 'cron', hour=hour, minute=minute, id=event["_id"])

	@classmethod
	def check_events(cls, readings):
		logger.info("checking events")
		cls._latest_readings = readings
		for event in cls._events:
			if not event["scheduled_time"]:
				cls._check_rules(event, readings)
	@classmethod
	def _check_rules(cls, event, readings, is_scheduled_time=False):
		logger.info("checking rules")
		if event["scheduled_time"] and event["logic"] == "AND" and not is_scheduled_time:
    			return
		logger.info("checking rules got past schedule logic")
		result = None
		for condition in event["conditions"]:
			subcondition = False
			if condition["type"] == "greater_than":
				logger.info(f"condition type: {condition['type']}, condition value {condition['value']}, readings value: {readings[condition['measurement']]}") 
				sub_condition = condition["value"] < readings[condition["measurement"]]
			elif condition["type"] == "less_than":
				logger.info(f"condition type: {condition['type']}, condition value {condition['value']}, readings value: {readings[condition['measurement']]}")
				sub_condition = condition["value"] > readings[condition["measurement"]]

			if not result:
				result = sub_condition
			else:
				if event["logic"] == "AND":
					result = result and sub_condition
				elif event["logic"] == "OR":
					result = result or sub_condition
			logger.info(result)

		logger.info(f"final result {result}")
		if result:
			cls._trigger_event(event)

	@staticmethod
	def _trigger_event(event):
		now = datetime.now(timezone.utc)
		last_triggered = event["last_triggered"]
		if last_triggered:
			if isinstance(last_triggered, str):
				last_triggered = datetime.fromisoformat(last_triggered)
			if last_triggered.tzinfo is None:
				last_triggered = last_triggered.replace(tzinfo=timezone.utc)
			if now - last_triggered < timedelta(hours=1):
				return

		logger.info(f"event triggered: {event['_id']}")
		for action_id in event["actions"]:
			ActionManager.trigger_action(action_id)

		now = now.isoformat()
		Event.update(event["_id"], {"last_triggered": now})
		event["last_triggered"] = now
		Notification.create(notification_type="event", entity_id=event["_id"], timestamp=now)

	@classmethod
	def delete_event(cls, event_id):
		cls._scheduler.remove_job(event_id)
		cls._events = [e for e in cls._events if e["_id"] != event_id]
