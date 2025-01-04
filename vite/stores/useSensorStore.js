import { defineStore } from 'pinia';

export const useSensorStore = defineStore('sensor', {
	state: () => ({
		sensors: {},
	}),
	getters: {
		sensorsObj() {
			return this.sensors;
		},
		SHT31() {
			return this.sensors.SHT31;
		},
		TSL2561() {
			return this.sensors.TSL2561;
		},
		SS() {
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
				return Promise.allSettled(Object.keys(this.sensors).map(sensorName => this.getReadings(sensorName)));
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