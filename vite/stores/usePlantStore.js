import { defineStore } from 'pinia';

export const usePlantStore = defineStore('plant', {
	state: () => ({
		plant: {},
	}),
	getters: {
		plantData() {
			return this.plant;
		}
	},
	actions: {
		getPlant() {
			return axios.get(host + '/get_plant')
			.then(({data}) => {
				Object.assign(this.plant, data);
			});
		},
	}
});