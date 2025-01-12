import { defineStore } from 'pinia';

export const useSensorStore = defineStore('sensor', {
	state: () => ({
		sensors: [],
	}),
	getters: {
		sensorsArr() {
			return this.sensors;
		},
		SHT31() {
			return this.sensors.find(s => s.name === 'SHT31');
		},
		TSL2561() {
			return this.sensors.find(s => s.name === 'TSL2561');
		},
		SS() {
			return this.sensors.find(s => s.name === 'SS');
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