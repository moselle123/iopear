import { defineStore } from 'pinia';

export const useActuatorStore = defineStore('actuator', {
	state: () => ({
		actuators: [],
	}),
	getters: {
		actuatorsObj() {
			let obj = {}
			this.actuators.forEach((action) => {
				obj[action._id] = {}
				Object.assign(obj[action._id], action);
				delete obj[action._id]._id;
			})
			return obj;
		},
	},
	actions: {
		getActuators() {
			return axios.get(host + '/get_actuators')
			.then(({data}) => {
				this.actuators = data;
			});
		},
	}
});