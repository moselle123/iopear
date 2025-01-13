<template>
	<el-text style="margin-bottom: 1em;">Alter thresholds below by dragging the slider to the desired range and click save changes to confirm the new settings.</el-text>
	<el-row class="configure-sensors grid" direction="vertical">
		<el-col v-for="sensor in sensors" :key="sensor" :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
			<el-card>
				<template #header>
					<el-row>
						<el-text size="large">{{ sensor.name }}</el-text>
						<el-tag v-if="sensor.name === 'SS'">Soil Moisture</el-tag>
						<el-tag v-if="sensor.name === 'SS'" type="danger">Soil Temperature</el-tag>
						<el-tag v-if="sensor.name === 'SHT31'" type="danger">Temperature</el-tag>
						<el-tag v-if="sensor.name === 'SHT31'">Humidity</el-tag>
						<el-tag v-if="sensor.name === 'TSL2561'" type="warning">Light Intensity</el-tag>
					</el-row>
				</template>
				<el-form label-position="left" label-width="150px">
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
					<el-form-item v-if="sensor.name === 'BMP280'" label="Barometric Pressure">
						<el-slider v-model="altered.BMP280.thresholds.barometric_pressure" range show-stops show-tooltip :min="900" :max="1100" :marks="marks.barometric_pressure" :step="10" />
					</el-form-item>
					<el-button @click="updateSensor(sensor.name)">Save Changes</el-button>
				</el-form>
			</el-card>
		</el-col>
	</el-row>
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

			let marks = {temperature: {5: '5°C', 45: '45°C'}, humidity: {0: '0%', 100: '100%'}, soil_moisture: {0: '0%', 100: '100%'}, soil_temperature:  {5: '5°C', 45: '45°C'}, light_intensity: {50: '50lx', 1000: '1000lx'}, barometric_pressure: {960: '960hPa', 1000: '1050hPa'}};
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
	},
};
</script>
<style lang="scss" scoped>
.configure-sensors {

}
</style>
