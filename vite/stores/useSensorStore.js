import { defineStore } from 'pinia';

export const useSensorStore = defineStore('sensor', {
	state: () => ({
		sensors: {},
	}),
	getters: {
		getSht31() {
			return this.sensors.SHT31;
		},
		getTsl2561() {
			return this.sensors.TSL2561;
		},
		getSs() {
			return this.sensors.SS;
		},
		getSoilMoistureReadings() {
			return this.sensors.SS.readings.filter(r => r.measurement === 'soil moisture');
		},
		getSoilTemperatureReadings() {
			return this.sensors.SS.readings.filter(r => r.measurement === 'soil temperature');
		},
		getHumidityReadings() {
			return this.sensors.SHT31.readings.filter(r => r.measurement === 'humidity');
		},
		getTemperatureReadings() {
			return this.sensors.SHT31.readings.filter(r => r.measurement === 'temperature');
		},
		getLuxReadings() {
			return this.sensors.TSL2561.readings.filter(r => r.measurement === 'lux');
		},
	},
	actions: {
		getSensors() {
			return axios.get(host + '/get_sensors')
			.then(({data}) => {
				data.forEach(sensor => {
					this.sensors[sensor.name] = {}
					this.sensors[sensor.name]._id = sensor._id;
					if (sensor.calibration) {
						this.sensors[sensor.name].calibration = sensor.calibration;
					}
				});
				Object.keys(this.sensors).forEach(sensor => this.getReadings(sensor));
			});
		},
		getReadings(sensorName) {
			return axios.get(host + '/sensor/' + sensorName + '/readings')
			.then(({data}) => {
				this.sensors[sensorName].readings = data;
			});
		},
	}
});