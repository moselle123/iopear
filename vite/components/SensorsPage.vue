<template>
	<el-container direction="vertical" class="sensors">
		<el-text class="title">Sensors</el-text>
		<el-text style="margin-bottom: 1em;">Alter thresholds below by dragging the slider to the desired range and click save changes to confirm the new settings.</el-text>
		<el-row class="grid" direction="vertical">
			<el-col v-for="sensor in sensors" :key="sensor" :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
				<el-card>
					<template #header>
						<el-row>
							<el-text size="large">{{ sensor.name }}</el-text>
							<el-tag v-if="sensor.name === 'SS'" effect="plain" class="soil-moisture">Soil Moisture</el-tag>
							<el-tag v-if="sensor.name === 'SS'" effect="plain" class="soil-temperature">Soil Temperature</el-tag>
							<el-tag v-if="sensor.name === 'SHT31'" effect="plain" class="temperature">Temperature</el-tag>
							<el-tag v-if="sensor.name === 'SHT31'" effect="plain" class="humidity">Humidity</el-tag>
							<el-tag v-if="sensor.name === 'TSL2561'" effect="plain" class="light-intensity">Light Intensity</el-tag>
							<el-tag v-if="sensor.name === 'SCD40'" effect="plain" class="co2">CO2</el-tag>
							<el-tag v-if="sensor.name === 'BMP280'" effect="plain" class="barometric-pressure">Barometric Pressure</el-tag>
						</el-row>
					</template>
					<el-form label-position="top" label-width="150px">
						<el-form-item :label="'Enable ' + sensor.name">
							<el-switch v-model="sensor.enabled" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'SS'"  label="Soil Moisture">
							<el-slider v-model="altered.SS.thresholds.soil_moisture" range show-stops show-tooltip :min="0" :max="100" :marks="marks.soil_moisture" :step="5" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'SS'" label="Soil Temperature">
							<el-slider  v-model="altered.SS.thresholds.soil_temperature" range show-stops show-tooltip :min="5" :max="45" :marks="marks.soil_temperature" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'SHT31'" label="Temperature">
							<el-slider  v-model="altered.SHT31.thresholds.temperature" range show-stops show-tooltip :min="5" :max="45" :marks="marks.temperature" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'SHT31'" label="Humidity">
							<el-slider  v-model="altered.SHT31.thresholds.humidity" range show-stops show-tooltip :min="0" :max="100" :marks="marks.humidity" :step="5" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'TSL2561'" label="Light Intensity">
							<el-slider v-model="altered.TSL2561.thresholds.light_intensity" range show-stops show-tooltip :min="50" :max="1000" :marks="marks.light_intensity" :step="50" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'SCD40'" label="CO2">
							<el-slider v-model="altered.SCD40.thresholds.co2" range show-stops show-tooltip :min="100" :max="1500" :marks="marks.co2" :step="100" />
						</el-form-item>
						<el-form-item v-if="sensor.name === 'BMP280'" label="Barometric Pressure">
							<el-slider v-model="altered.BMP280.thresholds.barometric_pressure" range show-stops show-tooltip :min="900" :max="1100" :marks="marks.barometric_pressure" :step="10" />
						</el-form-item>
					</el-form>
					<el-row justify="end">
						<el-button @click="updateSensor(sensor.name)" type="primary">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-242.7c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32L64 32zm0 96c0-17.7 14.3-32 32-32l192 0c17.7 0 32 14.3 32 32l0 64c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-64zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
							Save Changes
						</el-button>
					</el-row>
				</el-card>
			</el-col>
		</el-row>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			altered: {
				SHT31: {},
				TSL2561: {},
				SS: {},
				BMP280: {},
				SCD40: {},
			},
		};
	},
	computed: {
		sensors() {
			return this.$stores.sensorStore.sensorsArr;
		},
		marks() {
			let SHT31 = this.$stores.sensorStore.SHT31;
			let TSL2561 = this.$stores.sensorStore.TSL2561;
			let SS = this.$stores.sensorStore.SS;
			let BMP280 = this.$stores.sensorStore.BMP280;
			let SCD40 = this.$stores.sensorStore.SCD40;

			let marks = {temperature: {5: '5°C', 45: '45°C'}, humidity: {0: '0%', 100: '100%'}, soil_moisture: {0: '0%', 100: '100%'}, soil_temperature:  {5: '5°C', 45: '45°C'}, light_intensity: {50: '50lx', 1000: '1000lx'}, barometric_pressure: {900: '900hPa', 1100: '110hPa'}, co2: {100: '100ppm', 1500: '1500ppm'}};
			marks.temperature[SHT31.thresholds.temperature[0]] = SHT31.thresholds.temperature[0] + '°C';
			marks.temperature[SHT31.thresholds.temperature[1]] = SHT31.thresholds.temperature[1] + '°C';
			marks.humidity[SHT31.thresholds.humidity[0]] = SHT31.thresholds.humidity[0] + '%';
			marks.humidity[SHT31.thresholds.humidity[1]] = SHT31.thresholds.humidity[1] + '%';
			marks.soil_moisture[SS.thresholds.soil_moisture[0]] = SS.thresholds.soil_moisture[0] + '%';
			marks.soil_moisture[SS.thresholds.soil_moisture[1]] = SS.thresholds.soil_moisture[1] + '%';
			marks.soil_temperature[SS.thresholds.soil_temperature[0]] = SS.thresholds.soil_temperature[0] + '°C';
			marks.soil_temperature[SS.thresholds.soil_temperature[1]] = SS.thresholds.soil_temperature[1] + '°C';
			marks.light_intensity[TSL2561.thresholds.light_intensity[0]] = TSL2561.thresholds.light_intensity[0] + 'lx';
			marks.light_intensity[TSL2561.thresholds.light_intensity[1]] = TSL2561.thresholds.light_intensity[1] + 'lx';
			marks.barometric_pressure[BMP280.thresholds.barometric_pressure[0]] = BMP280.thresholds.barometric_pressure[0] + 'hPa';
			marks.barometric_pressure[BMP280.thresholds.barometric_pressure[1]] = BMP280.thresholds.barometric_pressure[1] + 'hPa';
			marks.co2[SCD40.thresholds.co2[0]] = SCD40.thresholds.co2[0] + 'ppm';
			marks.co2[SCD40.thresholds.co2[1]] = SCD40.thresholds.co2[1] + 'ppm';

			return marks;
		},
	},
	methods: {
		updateSensor(sensorName) {
			this.$stores.sensorStore.updateSensorSettings(sensorName, this.altered[sensorName]);
		},
	},
	beforeMount() {
		Object.assign(this.altered.SHT31, this.$stores.sensorStore.SHT31);
		Object.assign(this.altered.TSL2561, this.$stores.sensorStore.TSL2561);
		Object.assign(this.altered.SS, this.$stores.sensorStore.SS);
		Object.assign(this.altered.BMP280, this.$stores.sensorStore.BMP280);
		Object.assign(this.altered.SCD40, this.$stores.sensorStore.SCD40);
	},
};
</script>
<style lang="scss" scoped>
.sensors {
	.el-form {
		margin: 1em 1em 3em 1em;
	}
}
</style>
