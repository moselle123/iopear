from flask import current_app
from app.models import Sensor

class SensorRegistry:
    _registry = {}

    @classmethod
    def get_sensor(cls, name):
        if name in cls._registry:
            return cls._registry[name]

        sensor_data = current_app.config['DB']["sensors"].find_one({"name": name})
        if not sensor_data:
            return None

        sensor = Sensor(_id=str(sensor_data["_id"]), name=sensor_data["name"])
        cls._registry[name] = sensor
        return sensor

    @classmethod
    def attach_adafruit_instance(cls, name, adafruit_instance):
        sensor = cls.get_sensor(name)
        if sensor:
            sensor.set_adafruit_instance(adafruit_instance)
