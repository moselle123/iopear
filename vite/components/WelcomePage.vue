<template>
	<el-container class="welcome">
		<el-text size="large" class="title" type="primary">Welcome to ioPear!</el-text>
		<el-steps :active="step" align-center>
			<el-step title="Species" />
			<el-step title="Name" />
			<el-step title="Thresholds" />
			<el-step title="Calibrate" />
			<el-step title="Confirm" />
		</el-steps>
		<el-text v-if="step < 3" class="subtitle" size="large">Firstly we need to know some information about your plant...</el-text>
		<el-text v-else-if="step === 3" class="subtitle" size="large">Next we need to calibrate your soil moisture sensor...</el-text>
		<el-text v-else-if="step === 4" class="subtitle" size="large">Now confirm the details you've selected to save your plant.</el-text>
		<el-form label-width="auto" label-position="top">
			<el-form-item v-if="step === 0" label="What is the species of your plant?">
				<el-select v-model="plant.plantTypeId" placeholder="Select a species" @change="assignSettings">
					<el-option v-for="species in plantTypes" :key="species" :label="species.name" :value="species._id"/>
				</el-select>
			</el-form-item>
			<el-form-item v-if="step === 1" label="What would you like to call your plant?">
				<el-input v-model="plant.name" :placeholder="recommendedNames"/>
			</el-form-item>
			<template v-if="step === 2">
				<el-text>Recommended environmental settings for a {{ selectedPlantType.name }}. To customize, select a field and adjust the slider as desired.</el-text>
				<el-collapse accordion>
					<el-collapse-item :title="'Soil Moisture: ' +  plant.settings.SS.thresholds.soil_moisture[0] + ' - ' + plant.settings.SS.thresholds.soil_moisture[1] + ' (%)'" name="1">
						<el-slider v-model="plant.settings.SS.thresholds.soil_moisture" range show-stops show-tooltip :min="0" :max="100" :marks="marks.soil_moisture" :step="5" />
					</el-collapse-item>
					<el-collapse-item :title="'Soil Temperature: ' +  plant.settings.SS.thresholds.soil_temperature[0] + ' - ' + plant.settings.SS.thresholds.soil_temperature[1] + ' (°C)'" name="2">
						<el-slider v-model="plant.settings.SS.thresholds.soil_temperature" range show-stops show-tooltip :min="5" :max="45" :marks="marks.soil_temperature" />
					</el-collapse-item>
					<el-collapse-item :title="'Light Intensity: ' +  plant.settings.TSL2561.thresholds.light_intensity[0] + ' - ' + plant.settings.TSL2561.thresholds.light_intensity[1] + ' (lx)'" name="3">
						<el-slider v-model="plant.settings.TSL2561.thresholds.light_intensity" range show-stops show-tooltip :min="50" :max="1000" :marks="marks.light_intensity" :step="50" />
					</el-collapse-item>
					<el-collapse-item  :title="'Environmental Temperature: ' +  plant.settings.SHT31.thresholds.temperature[0] + ' - ' + plant.settings.SHT31.thresholds.temperature[1] + ' (°C)'" name="4">
						<el-slider v-model="plant.settings.SHT31.thresholds.temperature" range show-stops show-tooltip :min="5" :max="45" :marks="marks.temperature" />
					</el-collapse-item>
					<el-collapse-item  :title="'Humidity: ' +  plant.settings.SHT31.thresholds.humidity[0] + ' - ' + plant.settings.SHT31.thresholds.humidity[1] + ' (%)'" name="5">
						<el-slider v-model="plant.settings.SHT31.thresholds.humidity" range show-stops show-tooltip :min="0" :max="100" :marks="marks.humidity" :step="5" />
					</el-collapse-item>
					<el-collapse-item  :title="'Barometric Pressure: ' +  plant.settings.BMP280.thresholds.barometric_pressure[0] + ' - ' + plant.settings.BMP280.thresholds.barometric_pressure[1] + ' (%)'" name="6">
						<el-slider v-model="plant.settings.BMP280.thresholds.barometric_pressure" range show-stops show-tooltip :min="900" :max="1100" :marks="marks.barometric_pressure" :step="10" />
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
					<el-button type="primary" @click="getSoilMoistureReading">Measure Dry Level</el-button>
				</template>
				<template v-else-if="calibrationReadings.length === 1">
					<el-text size="large" tag="b">Step 2: Wet Calibration</el-text>
					<el-text>Now, place your soil moisture sensor in a glass of water. When it’s fully submerged, click below to take a maximum reading. Keep the sensor in the water until prompted.</el-text>
					<el-button type="primary" @click="getSoilMoistureReading">Measure Saturated Level</el-button>
				</template>
				<template v-else>
					<el-alert type="success" :closable="false" show-icon title="Your soil moisture sensor has now been calibrated! Click next to continue." />
				</template>
			</el-container>
			<el-container v-if="step === 4" class="confirm" direction="vertical" justify="space-evenly">
				<el-row justify="center">
					<el-col :xs="10" :sm="10" :md="10" :lg="10" :xl="10" class="keys">
						<el-text>Plant Type:</el-text>
						<el-text style="margin-bottom: 1em;">Plant Name:</el-text>
						<el-text>Soil Moisture Threshold:</el-text>
						<el-text>Soil Temperature Threshold:</el-text>
						<el-text>Humidity Threshold:</el-text>
						<el-text>Temperature Threshold:</el-text>
						<el-text>Light Intensity Threshold:</el-text>
						<el-text>CO2 Threshold:</el-text>
						<el-text>Barometric Pressure Threshold:</el-text>
					</el-col>
					<el-col class="values" :xs="5" :sm="5" :md="5" :lg="5" :xl="5">
						<el-text>{{ selectedPlantType.name }}</el-text>
						<el-text style="margin-bottom: 1em;">{{ plant.name }}</el-text>
						<el-text>{{ plant.settings.SS.thresholds.soil_moisture }}</el-text>
						<el-text>{{ plant.settings.SS.thresholds.soil_temperature }}</el-text>
						<el-text>{{ plant.settings.SHT31.thresholds.humidity }}</el-text>
						<el-text>{{ plant.settings.SHT31.thresholds.temperature }}</el-text>
						<el-text>{{ plant.settings.TSL2561.thresholds.light_intensity }}</el-text>
						<el-text></el-text>
						<el-text>{{ plant.settings.BMP280.thresholds.barometric_pressure }}</el-text>
					</el-col>
				</el-row>
			</el-container>
			<el-row justify="space-between" class="navigation-buttons">
				<el-button @click="previousStep" :disabled="step === 0">Back</el-button>
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
				settings: null,
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
			let marks = {temperature: {5: '5°C', 45: '45°C'}, humidity: {0: '0%', 100: '100%'}, soil_moisture: {0: '0%', 100: '100%'}, soil_temperature:  {5: '5°C', 45: '45°C'}, light_intensity: {50: '50lx', 1000: '1000lx'}, barometric_pressure: {960: '960hPa', 1060: '1050hPa'}};
			marks.temperature[this.selectedPlantType?.thresholds.temperature[0]] = this.selectedPlantType?.thresholds.temperature[0] + '°C';
			marks.temperature[this.selectedPlantType?.thresholds.temperature[1]] = this.selectedPlantType?.thresholds.temperature[1] + '°C';
			marks.humidity[this.selectedPlantType?.thresholds.humidity[0]] = this.selectedPlantType?.thresholds.humidity[0] + '%';
			marks.humidity[this.selectedPlantType?.thresholds.humidity[1]] = this.selectedPlantType?.thresholds.humidity[1] + '%';
			marks.soil_moisture[this.selectedPlantType?.thresholds.soil_moisture[0]] = this.selectedPlantType?.thresholds.soil_moisture[0] + '%';
			marks.soil_moisture[this.selectedPlantType?.thresholds.soil_moisture[1]] = this.selectedPlantType?.thresholds.soil_moisture[1] + '%';
			marks.soil_temperature[this.selectedPlantType?.thresholds.soil_temperature[0]] = this.selectedPlantType?.thresholds.soil_temperature[0] + '°C';
			marks.soil_temperature[this.selectedPlantType?.thresholds.soil_temperature[1]] = this.selectedPlantType?.thresholds.soil_temperature[1] + '°C';
			marks.light_intensity[this.selectedPlantType?.thresholds.light_intensity[0]] = this.selectedPlantType?.thresholds.light_intensity[0] + 'lx';
			marks.light_intensity[this.selectedPlantType?.thresholds.light_intensity[1]] = this.selectedPlantType?.thresholds.light_intensity[1] + 'lx';
			marks.barometric_pressure[this.selectedPlantType?.thresholds.barometric_pressure[0]] = this.selectedPlantType?.thresholds.barometric_pressure[0] + 'hPa';
			marks.barometric_pressure[this.selectedPlantType?.thresholds.barometric_pressure[1]] = this.selectedPlantType?.thresholds.barometric_pressure[1] + 'hPa';

			return marks;
		},
	},
	methods: {
		assignSettings() {
			return this.plant.settings = {
				SHT31: {
					enabled: true,
					thresholds: {
						temperature: this.selectedPlantType.thresholds.temperature,
						humidity: this.selectedPlantType.thresholds.humidity,
					},
				},
				TSL2561: {
					enabled: true,
					thresholds: {
						light_intensity: this.selectedPlantType.thresholds.light_intensity,
					},
				},
				BMP280: {
					enabled: true,
					thresholds: {
						barometric_pressure: this.selectedPlantType.thresholds.barometric_pressure,
					},
				},
				SS: {
					enabled: true,
					thresholds: {
						soil_moisture: this.selectedPlantType.thresholds.soil_moisture,
						soil_temperature: this.selectedPlantType.thresholds.soil_temperature,
					},
				},
			};
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
		this.$stores.plantStore.getPlantTypes()
		.then(data => this.plantTypes = data);
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

	.title, .subtitle {
		align-self: center !important;
	}

	.el-steps {
		margin: 2em 0;
	}

	.el-form {
		margin: 2em 0;

		.el-form-item {
			margin-bottom: 4em;
		}

		.el-collapse {
			margin: 1em 0;
		}

		.calibration {
			gap: 2em;

			margin: 2em 0;

			.el-button {
				width: 12em !important;
				margin: 0 auto;
			}
		}

		.confirm {
			.keys {
				font-weight: 400;
			}
		}
	}


	.navigation-buttons {
		margin-top: 2em;
	}


}
</style>
