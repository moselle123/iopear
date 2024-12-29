<template>
	<el-container class="welcome">
		<el-text size="large" type="primary">Welcome to ioPear!</el-text>
		<el-text>Firstly we need to know some information about your plant...</el-text>
		<el-steps :active="step" align-center>
			<el-step title="Species" />
			<el-step title="Name" />
			<el-step title="Thresholds" />
		</el-steps>
		<el-form label-width="auto" label-position="top">
			<el-form-item v-if="step === 0" label="What is the species of your plant?">
				<el-select v-model="plant.plantTypeId" placeholder="Select a species" @change="assignThresholds">
					<el-option v-for="species in plantTypes" :key="species" :label="species.name" :value="species._id"/>
				</el-select>
			</el-form-item>
			<el-form-item v-if="step === 1" label="What would you like to call your plant?">
				<el-input v-model="plant.name" :placeholder="recommendedNames"/>
			</el-form-item>
			<template v-if="step === 2">
				<el-text>Recommended environmental settings for a {{ selectedPlantType.name }}. To customize, select a field and adjust the slider as desired.</el-text>
				<el-collapse accordion>
					<el-collapse-item :title="'Soil Moisture: ' +  plant.thresholds.soil_moisture[0] + ' - ' + plant.thresholds.soil_moisture[1] + ' (%)'" name="1">
						<el-slider v-model="plant.thresholds.soil_moisture" range show-stops show-tooltip :min="0" :max="100" :marks="marks.soil_moisture" :step="5" />
					</el-collapse-item>
					<el-collapse-item :title="'Soil Temperature: ' +  plant.thresholds.soil_temperature[0] + ' - ' + plant.thresholds.soil_temperature[1] + ' (°C)'" name="2">
						<el-slider v-model="plant.thresholds.soil_temperature" range show-stops show-tooltip :min="5" :max="45" :marks="marks.soil_temperature" />
					</el-collapse-item>
					<el-collapse-item :title="'Light Intensity: ' +  plant.thresholds.lux[0] + ' - ' + plant.thresholds.lux[1] + ' (lx)'" name="3">
						<el-slider v-model="plant.thresholds.lux" range show-stops show-tooltip :min="50" :max="1000" :marks="marks.lux" :step="50" />
					</el-collapse-item>
					<el-collapse-item  :title="'Environmental Temperature: ' +  plant.thresholds.temperature[0] + ' - ' + plant.thresholds.temperature[1] + ' (°C)'" name="4">
						<el-slider v-model="plant.thresholds.temperature" range show-stops show-tooltip :min="5" :max="45" :marks="marks.temperature" />
					</el-collapse-item>
					<el-collapse-item  :title="'Humidity: ' +  plant.thresholds.humidity[0] + ' - ' + plant.thresholds.humidity[1] + ' (%)'" name="5">
						<el-slider v-model="plant.thresholds.humidity" range show-stops show-tooltip :min="0" :max="100" :marks="marks.humidity" :step="5" />
					</el-collapse-item>
				</el-collapse>
			</template>
			<el-row justify="space-between">
				<el-button @click="previousStep">Back</el-button>
				<el-button @click="nextStep" :disabled="(step === 0 && !plant.plantTypeId) || (step === 1 && !plant.name)">Next</el-button>
			</el-row>
		</el-form>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			plantTypes: null,
			plant: {
				name: null,
				plantTypeId: null,
				thresholds: {
					temperature: null,
					humidity: null,
					soil_moisture: null,
					soil_temperature: null,
					lux: null,
				},
			},
			step: 0,
		};
	},
	computed: {
		selectedPlantType() {
			return this.plantTypes.find((type) => type._id === this.plant.plantTypeId);
		},
		recommendedNames() {
			if (!this.selectedPlantType?.nicknames.length) {
				return 'Choose a name for your plant'
			} else if (this.selectedPlantType?.nicknames.length === 1) {
				return 'Common nicknames: ' + this.selectedPlantType?.nicknames[0];
			}
			return 'Common nicknames: ' + this.selectedPlantType?.nicknames[0] + ', ' + this.selectedPlantType?.nicknames[1];
		},
		marks() {
			let marks = {temperature: {5: '5°C', 45: '45°C'}, humidity: {0: '0%', 100: '100%'}, soil_moisture: {0: '0%', 100: '100%'}, soil_temperature:  {5: '5°C', 45: '45°C'}, lux: {50: '50lx', 1000: '1000lx'}};
			marks.temperature[this.selectedPlantType?.thresholds.temperature[0]] = this.selectedPlantType?.thresholds.temperature[0] + '°C';
			marks.temperature[this.selectedPlantType?.thresholds.temperature[1]] = this.selectedPlantType?.thresholds.temperature[1] + '°C';
			marks.humidity[this.selectedPlantType?.thresholds.humidity[0]] = this.selectedPlantType?.thresholds.humidity[0] + '%';
			marks.humidity[this.selectedPlantType?.thresholds.humidity[1]] = this.selectedPlantType?.thresholds.humidity[1] + '%';
			marks.soil_moisture[this.selectedPlantType?.thresholds.soil_moisture[0]] = this.selectedPlantType?.thresholds.soil_moisture[0] + '%';
			marks.soil_moisture[this.selectedPlantType?.thresholds.soil_moisture[1]] = this.selectedPlantType?.thresholds.soil_moisture[1] + '%';
			marks.soil_temperature[this.selectedPlantType?.thresholds.soil_temperature[0]] = this.selectedPlantType?.thresholds.soil_temperature[0] + '°C';
			marks.soil_temperature[this.selectedPlantType?.thresholds.soil_temperature[1]] = this.selectedPlantType?.thresholds.soil_temperature[1] + '°C';
			marks.lux[this.selectedPlantType?.thresholds.lux[0]] = this.selectedPlantType?.thresholds.lux[0] + 'lx';
			marks.lux[this.selectedPlantType?.thresholds.lux[1]] = this.selectedPlantType?.thresholds.lux[1] + 'lx';

			return marks;
		}
	},
	methods: {
		getPlantTypes() {
			return axios.get('http://' + host + '/get_plant_types')
			.then(({data}) => {
				this.plantTypes = data;
				Object.assign(this.plant.plantType, data[0]);
			});
		},
		assignThresholds() {
			Object.assign(this.plant.thresholds, this.selectedPlantType.thresholds);
		},
		nextStep() {
			this.step++;
		},
		previousStep() {
			this.step--;
		},
		createPlant() {
			axios.post('http://' + host + '/create_plant', this.plant)
			.then(({data}) => {
				setTimeout(() => {
					this.$emit('setPlant', data);
				}, 1000);
			});
		},
	},
	beforeMount() {
		this.getPlantTypes();
	},
};
</script>
<style lang="scss" scoped>
.welcome {
	flex-direction: column;
	gap: 1em;

	margin: auto;
	max-width: 600px;
	width: 60%;

	.el-form {
		margin-top: 3em;
		.el-form-item {
			margin-bottom: 4em;
		}

		.el-collapse {
			margin: 1em 0;
		}
	}
}
</style>
