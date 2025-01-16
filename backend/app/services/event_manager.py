from datetime import datetime, timezone, timedelta
from app.models.event import Event

class EventManager():
	@staticmethod
	def checkEvents(measurement, value):
		events = Event.get_events_by_measurement(measurement)

		for event in events:
			condition_met = False
			if event["condition"] == "greater_than" and value > event["threshold"]:
				condition_met = True
			elif event["condition"] == "less_than" and value < event["threshold"]:
				condition_met = True


			if condition_met:
				last_triggered = event["last_triggered"]
				if last_triggered:
					if last_triggered.tzinfo is None:
						last_triggered = last_triggered.replace(tzinfo=timezone.utc)

					if (datetime.now(timezone.utc) - last_triggered) < timedelta(hours=1):
						continue

				now =  datetime.now(timezone.utc)
				Event.create_event_instance(event["_id"], value, now)
				Event.update_last_triggered(event["_id"], now)

