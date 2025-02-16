from flask import current_app

class Actuator:
	def create(self, name, pin):
		result = current_app.config['DB']["actuator"].insert_one({"name": name, "pin": pin})
		return result.inserted_id

	@staticmethod
	def get_actuators():
		return current_app.config['DB']["actuator"].find()
