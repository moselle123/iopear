from datetime import datetime, timezone
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
				event_instance = {
					"event_id": event["_id"],
					"sensor_id": event["sensor_id"],
					"value": value,
					"timestamp": datetime.now(timezone.utc)
				}

				Event.create_event_instance(event_instance)
