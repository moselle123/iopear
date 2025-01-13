import { defineStore } from 'pinia';

export const useSensorStore = defineStore('sensor', {
	state: () => ({
		sensors: [],
	}),
	getters: {
		sensorsArr() {
			return this.sensors;
		},
		sensorsObj() {
			let obj = {};
			this.sensors.forEach((sensor) => {
				obj[sensor.name] = sensor;
				delete obj[sensor.name].name;

			});
			return obj;
		},
		sensorsByMeasurement() {
			return {
				temperature: this.sensors.find(s => s.name === 'SHT31'),
				humidity: this.sensors.find(s => s.name === 'SHT31'),
				soil_moisture: this.sensors.find(s => s.name === 'SS'),
				soil_temperature: this.sensors.find(s => s.name === 'SS'),
				barometric_pressure:this.sensors.find(s => s.name === 'BMP280'),
				light_intensity: this.sensors.find(s => s.name === 'TSL2561'),
			};
		},
	},
	actions: {
		getSensors() {
			return axios.get(host + '/get_sensors')
			.then(({data}) => {
				this.sensors = data;
			});
		},
		getReadingsByDateRange(sensorName, startDate, endDate, measurement) {
			return axios.get(host + '/sensor/' + sensorName + '/readings_by_date_range', { params: { start_date: startDate, end_date: endDate, measurement: measurement } })
			.then(res =>  res.data);
		},
		updateSensorSettings(sensorName, newSensorObj) {
			let settings = { enabled: newSensorObj.enabled, thresholds: newSensorObj.thresholds };
			return axios.put(host + '/sensor/' + sensorName + '/update_settings', settings)
			.then(() => {
				this.getSensors();
			});
		},
	}
});