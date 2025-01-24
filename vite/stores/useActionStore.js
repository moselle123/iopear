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
		createAction(action) {
			return axios.post(host + '/create_action', action)
			.then(() => this.getActions());
		},
		updateAction(action) {
			return axios.put(host + '/update_action/' + action._id, {actuator_id: action.actuator_id, actuator_state: action.actuator_state, duration: action?.duration ? Number(action.threshold) : null})
			.then(() => this.getActions());
		},
		deleteAction(action) {
			return axios.delete(host + '/delete_action/' + action._id)
			.then(() => this.getActions());
		},
	},
});