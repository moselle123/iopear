import { defineStore } from 'pinia';

export const useActuatorStore = defineStore('actuator', {
	state: () => ({
		actuators: [],
	}),
	getters: {
		actuatorsArr() {
			return this.actuators;
		},
	},
	actions: {
		getActuators() {
			return axios.get(host + '/get_actuators')
			.then(({data}) => {
				this.actuators = data;
			});
		},
		getActuatorStates() {
			window.socket.on("actuator-update", (data) => {
				console.debug('actuator update', data);
				this.actuator[data.actuator_id] = data.actuator_state;
			});
		},
	},
});