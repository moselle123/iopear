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
			});
		},
		getReadingsByDateRange(sensorName, startDate, endDate, measurement) {
			return axios.get(host + '/sensor/' + sensorName + '/readings_by_date_range', { params: { start_date: startDate, end_date: endDate, measurement: measurement } })
			.then(res =>  res.data);
		},
	}
});