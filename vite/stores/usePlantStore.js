import { defineStore } from 'pinia';

export const usePlantStore = defineStore('plant', {
	state: () => ({
		plant: {},
		plantType: {},
	}),
	getters: {
		plantData() {
			return this.plant;
		},
		plantTypeData() {
			return this.plantType;
		},
	},
	actions: {
		getPlant() {
			return axios.get(host + '/get_plant')
			.then(({data}) => {
				Object.assign(this.plant, data);
				this.getPlantType();
			});
		},
		getPlantType() {
			return axios.get(host + '/get_plant_type/' + this.plant.plant_type_id)
			.then(({data}) => {
				Object.assign(this.plantType, data);
			});
		},
	}
});