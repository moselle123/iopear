<template>
	<el-container class="dashboard" direction="vertical" justify="space-between">
		<el-text class="title">{{ plant?.name }}</el-text>
		<el-text>{{ plantType?.description }}</el-text>
		<el-row class="grid" justify="space-between">
			<el-row justify="space-evenly" align="middle">
				<el-countdown format="DD [days] HH:mm:ss" :value="soilMoisturePrediction">
					<template #title><el-text>Estimated Time Until Next Watering</el-text></template>
				</el-countdown>
				<el-check-tag v-model="growLight.state" class="actuator-button light" :disabled="! growLight" @change="toggleGrowLight" :style="growLight?.state ? '' : { opacity: 0.5 }">
					<div class="name">Grow Light</div>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M297.2 248.9C311.6 228.3 320 203.2 320 176c0-70.7-57.3-128-128-128S64 105.3 64 176c0 27.2 8.4 52.3 22.8 72.9c3.7 5.3 8.1 11.3 12.8 17.7c0 0 0 0 0 0c12.9 17.7 28.3 38.9 39.8 59.8c10.4 19 15.7 38.8 18.3 57.5L109 384c-2.2-12-5.9-23.7-11.8-34.5c-9.9-18-22.2-34.9-34.5-51.8c0 0 0 0 0 0s0 0 0 0c-5.2-7.1-10.4-14.2-15.4-21.4C27.6 247.9 16 213.3 16 176C16 78.8 94.8 0 192 0s176 78.8 176 176c0 37.3-11.6 71.9-31.4 100.3c-5 7.2-10.2 14.3-15.4 21.4c0 0 0 0 0 0s0 0 0 0c-12.3 16.8-24.6 33.7-34.5 51.8c-5.9 10.8-9.6 22.5-11.8 34.5l-48.6 0c2.6-18.7 7.9-38.6 18.3-57.5c11.5-20.9 26.9-42.1 39.8-59.8c0 0 0 0 0 0s0 0 0 0s0 0 0 0c4.7-6.4 9-12.4 12.7-17.7zM192 128c-26.5 0-48 21.5-48 48c0 8.8-7.2 16-16 16s-16-7.2-16-16c0-44.2 35.8-80 80-80c8.8 0 16 7.2 16 16s-7.2 16-16 16zm0 384c-44.2 0-80-35.8-80-80l0-16 160 0 0 16c0 44.2-35.8 80-80 80z"/></svg>
					<div class="state">{{ growLight?.state ? 'ON' : 'OFF' }}</div>
				</el-check-tag>
			</el-row>
			<template v-for="(sensor, key) in sensors" :key="key">
				<el-col v-if="sensor.enabled" :xs="24" :sm="12" :md="12" :lg="8" :xl="8">
					<line-chart :sensorName="sensor.name" :dateRange="[startDate, endDate]" step="minute" :measurement="key" />
				</el-col>
			</template>
		</el-row>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			endDate: moment().tz('Europe/London').toISOString(),
			startDate: moment().tz('Europe/London').subtract(1, 'hour').toISOString(),
			soilMoisturePrediction: null,
		};
	},
	computed: {
		plant() {
			return this.$stores.plantStore.plantData;
		},
		plantType() {
			return this.$stores.plantStore.plantTypeData;
		},
		sensors() {
			return this.$stores.sensorStore.sensorsByMeasurement;
		},
		growLight() {
			return this.$stores.actuatorStore.growLight;
		},
		waterPump() {
			return this.$stores.actuatorStore.waterPump;
		},
		humidifier() {
			return this.$stores.actuatorStore.humidifier;
		},
	},
	methods: {
		toggleGrowLight() {
			this.$stores.actionStore.triggerAction(this.growLight._id, ! this.growLight.state);
		},
		predictSoilMoisture() {
			return axios.get(host + '/predict/')
			.then(({data}) => this.soilMoisturePrediction = Date(data));
		},
	},
	mounted() {
		this.predictSoilMoisture();
	},
};
</script>
<style lang="scss">
.dashboard {
	gap: 1em;

	.actuator-button {
		display: flex;
		flex-direction: column;
		justify-content: space-evenly;
		gap: 7px;

		width: 6em !important;
		margin: 1em 0;

		box-shadow: var(--el-box-shadow-light);

		cursor: pointer;

		.name, .state {
			font-weight: 400;
			margin: auto;
		}

		.name {
			font-size: 0.9em;
		}

		svg {
			height: 2em !important;
		}

		&:hover {
			opacity: 0.8;
		}

		&.light {
			color: var(--light-intensity) !important;
			background-color: #f3d7c0;;
			border: 1px solid var(--light-intensity);

			svg {
				fill: var(--light-intensity);
			}
		}
	}

	.el-statistic {
		text-align: center;
	}
}
</style>
