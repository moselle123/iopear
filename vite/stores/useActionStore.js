import { defineStore } from 'pinia';

export const useActionStore = defineStore('action', {
	state: () => ({
		actions: [],
	}),
	getters: {
		actionsArr() {
			return this.actions;
		},
		actionsObj() {
			let obj = {}
			this.actions.forEach((action) => {
				obj[action._id] = {}
				Object.assign(obj[action._id], action);
				delete obj[action._id]._id;
			})
			return obj;
		},
	},
	actions: {
		getActions() {
			return axios.get(host + '/get_actions')
			.then(({data}) => {
				this.actions = data;
			});
		},
		triggerAction(actuator_id, state) {
			let action = this.actions.find((action) => action.actuator_id === actuator_id && action.actuator_state === state)
			socket.emit('trigger-action', action._id);
		},
	},
});