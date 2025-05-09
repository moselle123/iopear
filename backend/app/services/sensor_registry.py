from app.models import Sensor

class SensorRegistry:
	_registry = {}

	@classmethod
	def get_sensor(cls, name):
		if name in cls._registry:
			return cls._registry[name]

		sensor = Sensor.create(name)
		cls._registry[name] = sensor
		return sensor

	@classmethod
	def get_existing_sensor(cls, name):
		if name in cls._registry:
			return cls._registry[name]
		return None

	@classmethod
	def attach_adafruit_instance(cls, name, adafruit_instance):
		sensor = cls.get_sensor(name)
		if sensor:
			sensor.adafruit_instance = adafruit_instance

	@classmethod
	def attach_adafruit_instance(cls, name, adafruit_instance):
		sensor = cls.get_sensor(name)
		if sensor:
			sensor.adafruit_instance = adafruit_instance

	@classmethod
	def initialise_settings(cls, settings):
		for key, value in settings.items():
			cls.get_sensor(key).update_settings(value["enabled"], value["thresholds"])
