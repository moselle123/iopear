import { defineStore } from 'pinia';

export const useSensorStore = defineStore('sensor', {
	state: () => ({
		sensors: [],
	}),
	getters: {
		sensorsArr() {
			return this.sensors;
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
		SHT31() {
			return this.sensors.find(s => s.name === 'SHT31');
		},
		TSL2561() {
			return this.sensors.find(s => s.name === 'TSL2561');
		},
		BMP280() {
			return this.sensors.find(s => s.name === 'BMP280');
		},
		SS() {
			return this.sensors.find(s => s.name === 'SS');
		},
		SCD40() {
			return this.sensors.find(s => s.name === 'SCD40');
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