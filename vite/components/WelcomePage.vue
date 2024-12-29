<template>
	<el-container class="welcome">
		<el-text size="large" type="primary">Welcome to ioPear!</el-text>
		<el-steps :active="step" align-center>
			<el-step title="Species" />
			<el-step title="Name" />
			<el-step title="Thresholds" />
			<el-step title="Calibrate" />
			<el-step title="Confirm" />
		</el-steps>
		<el-text v-if="step < 3" size="large">Firstly we need to know some information about your plant...</el-text>
		<el-text v-else-if="step === 3" size="large">Next we need to calibrate your soil moisture sensor...</el-text>
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
			<el-container v-if="step === 3" class="calibration" direction="vertical">
				<!-- <template v-if="calibrating">
					<el-progress type="circle" :percentage="calibrationProgress" :status="calibrationProgress < 100 ? 'active' : 'success'" />
				</template> -->
				<template v-if=" ! calibrationReadings.length">
					<el-text size="large" tag="b">Step 1: Dry Calibration</el-text>
					<el-text>Make sure your soil moisture sensor is completely dry and removed from any soil. When ready, click below to take a baseline reading.</el-text>
					<el-button @click="getSoilMoistureReading">Measure Dry Level</el-button>
				</template>
				<template v-else-if="calibrationReadings.length === 1">
					<el-text size="large" tag="b">Step 2: Wet Calibration</el-text>
					<el-text>Now, place your soil moisture sensor in a glass of water. When it’s fully submerged, click below to take a maximum reading. Keep the sensor in the water until prompted.</el-text>
					<el-button @click="getSoilMoistureReading">Measure Saturated Level</el-button>
				</template>
				<template v-else>
					<el-text>Your soil moisture sensor has now been calibrated! Click next to continue.</el-text>
				</template>
			</el-container>
			<el-container v-if="step === 4" class="confirm" direction="vertical">
				<el-text tag="ins">Plant Details:</el-text>
				<el-text>Plant Type: {{ plantTypes.name }}</el-text>
				<el-text>Plant Name: {{ plant.name }}</el-text>
				<el-text tag="ins">Thresholds:</el-text>
				<el-text>Soil Moisture: {{ plant.thresholds.soil_moisture }}</el-text>
				<el-text>Soil Temperature: {{ plant.thresholds.soil_temperature }}</el-text>
				<el-text>Humidity: {{ plant.thresholds.humidity }}</el-text>
				<el-text>Air Temperature: {{ plant.thresholds.temperature }}</el-text>
				<el-text>Light Intensity: {{ plant.thresholds.lux }}</el-text>
				<el-text>CO2: </el-text>
				<el-text>Barometric Pressure:</el-text>
			</el-container>
			<el-row justify="space-between">
				<el-button @click="previousStep">Back</el-button>
				<el-button v-if="step < 4" @click="nextStep" :disabled="(step === 0 && !plant.plantTypeId) || (step === 1 && !plant.name)">Next</el-button>
				<el-button v-else @click="createPlant">Confirm</el-button>
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
			calibrationReadings: [],
			calibrating: false,
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
			return axios.get(host + '/get_plant_types')
			.then(({data}) => {
				this.plantTypes = data;
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
			axios.post(host + '/create_plant', this.plant)
			.then(({data}) => {
				setTimeout(() => {
					this.$emit('setupComplete', data);
				}, 1000);
			});
		},
		getSoilMoistureReading() {
			this.calibrating = true;
			return axios.get(host + '/get_calibration_reading')
			.then(({data}) => {
				this.calibrationReadings.push(data.soil_moisture);
				if (this.calibrationReadings .length == 2) {
					this.calibrateSensor();
				}
				this.calibrating = false;
			})
			.catch(() => {
				this.calibrating = false;
			});
		},
		calibrateSensor() {
			return axios.post(host + '/calibrate_soil_moisture_sensor', this.calibrationReadings)
			.catch((err) => {
				console.error('Error calibrating soil moisture sensor:', err);
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

	.el-steps {
		margin: 2em 0;
	}

	.el-form {
		margin-top: 3em;
		.el-form-item {
			margin-bottom: 4em;
		}

		.el-collapse {
			margin: 1em 0;
		}

		.calibration {
			gap: 2em;

			margin: 2em 0;
		}
	}
}
</style>
