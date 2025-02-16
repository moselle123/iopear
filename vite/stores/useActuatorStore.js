import { defineStore } from 'pinia';

export const useActuatorStore = defineStore('actuator', {
	state: () => ({
		actuators: [],
	}),
	getters: {
		actuatorsArr() {
			return this.actuators;
		},
		actuatorsObj() {
			let obj = {}
			this.actions.forEach((actuator) => {
				obj[actuator._id] = {}
				Object.assign(obj[actuator._id], actuator);
				delete obj[actuator._id]._id;
			})
			return obj;
		},
		growLight() {
			return this.actuators.find((actuator) => actuator.name === 'Grow Light');
		},
		humidifier() {
			return this.actuators.find((actuator) => actuator.name === 'Humidifier');
		},
		waterPump() {
			return this.actuators.find((actuator) => actuator.name === 'Water Pump');
		},
	},
	actions: {
		getActuators() {
			return axios.get(host + '/get_actuators')
			.then(({data}) => {
				this.actuators = data;
			});
		},
		updateActuatorState(data) {
			let actuator = this.actuators.find((actuator) => actuator._id === data.actuator_id);
			actuator.state = data.state;
		},
	},
});