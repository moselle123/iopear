from bson import ObjectId
from flask import current_app
from datetime import datetime, timezone, timedelta

class Reading:
	@staticmethod
	def create(sensor_id, measurement, unit, value, calibration=None):
		if calibration and measurement == "soil_moisture":
			value = (value - calibration['min']) / (calibration['max'] - calibration['min']) * 100
			value = max(0, min(100, value))

		reading = {
			"sensor_id": ObjectId(sensor_id),
			"timestamp": datetime.now(timezone.utc),
			"value": value,
			"unit": unit,
			"measurement": measurement,
		}

		current_app.config['DB']["reading"].insert_one(reading)

	@staticmethod
	def get_readings(sensor_id, limit=100, skip=0):
		readings_cursor = current_app.config['DB']["reading"].find({"sensor_id": ObjectId(sensor_id)}).sort("timestamp", -1).skip(skip).limit(limit)

		return [
			{
				"_id": str(reading["_id"]),
				"sensor_id": str(reading["sensor_id"]),
				"timestamp": reading["timestamp"].isoformat(),
				"value": reading["value"],
				"unit": reading["unit"],
				"measurement": reading["measurement"],
			}
			for reading in readings_cursor
		]

	def get_readings_by_date_range(sensor_id, start_date, end_date, measurement):
		duration = (end_date - start_date).total_seconds() / 86400
		if duration <= 1:
			aggregation = "minute"
		elif duration <= 7:
			aggregation = "hour"
		elif duration <= 30:
			aggregation = "day"
		else:
			aggregation = "month"

		time_fields = {
			"minute": {"minute": {"$minute": "$timestamp"}, "hour": {"$hour": "$timestamp"}, "day": {"$dayOfMonth": "$timestamp"}, "month": {"$month": "$timestamp"}, "year": {"$year": "$timestamp"}},
			"hour": {"hour": {"$hour": "$timestamp"}, "day": {"$dayOfMonth": "$timestamp"}, "month": {"$month": "$timestamp"}, "year": {"$year": "$timestamp"}},
			"day": {"day": {"$dayOfMonth": "$timestamp"}, "month": {"$month": "$timestamp"}, "year": {"$year": "$timestamp"}},
			"month": {"month": {"$month": "$timestamp"}, "year": {"$year": "$timestamp"}}
		}

		pipeline = [
			{
				"$match": {
					"sensor_id": ObjectId(sensor_id),
					"timestamp": {"$gte": start_date, "$lte": end_date},
					"measurement": measurement,
				},
			},
			{
				"$group": {
					"_id": time_fields[aggregation],
					"timestamp": {"$min": "$timestamp"},
					"value": {"$avg": "$value"},
					"unit": {"$first": "$unit"},
					"measurement": {"$first": "$measurement"},
					"sensor_id": {"$first": "$sensor_id"},
				},
			},
			{
				"$sort": {"timestamp": 1},
			}
		]

		results = list(current_app.config['DB']["reading"].aggregate(pipeline))

		return [
			{
				"_id": str(result["_id"]),
				"sensor_id": str(result["sensor_id"]),
				"timestamp": result["timestamp"].isoformat(),
				"value": result["value"],
				"unit": result["unit"],
				"measurement": result["measurement"],
			}
			for result in results
		]

	def get_readings_by_measurement(sensor_id, measurement, limit=100, skip=0):
		readings_cursor = current_app.config['DB']["reading"].find(
			{"sensor_id": ObjectId(sensor_id), "measurement": measurement}
		).sort("timestamp", -1).skip(skip).limit(limit)

		return [
			{
				"_id": str(reading["_id"]),
				"sensor_id": str(reading["sensor_id"]),
				"timestamp": reading["timestamp"].isoformat(),
				"value": reading["value"],
				"unit": reading["unit"],
				"measurement": reading["measurement"],
			}
			for reading in readings_cursor
		]

	@staticmethod
	def get_statistics():
		end_date = datetime.utcnow()
		start_date = end_date - timedelta(days=7)

		pipeline = [
			{
				"$match": {
					"timestamp": {"$gte": start_date, "$lte": end_date},
				},
			},
			{
				"$group": {
					"_id": "$measurement",
					"count": {"$sum": 1},
					"average": {"$avg": "$value"},
					"min": {"$min": "$value"},
					"max": {"$max": "$value"},
					"std_dev": {"$stdDevPop": "$value"},
				},
			},
		]

		results = list(current_app.config['DB']["reading"].aggregate(pipeline))

		if not results:
			return None

		stats = {}
		for result in results:
			stats[result["_id"]] = {
				"min": round(result["min"], 2),
				"max": round(result["max"], 2),
				"average": round(result["average"], 2),
			}

		return stats
