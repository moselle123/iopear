<template>
	<el-container class="data" direction="vertical">
		<el-text class="title">Data</el-text>
		<el-tabs v-model="activeTab">
			<el-tab-pane v-for="(sensor, key) in sensors" :key="key" :label="tabData[key].label" :name="key">
				<el-row justify="space-between">
					<el-col :xs="24" :sm="24" :md="7" :lg="7" :xl="7">
						<el-text>{{ tabData[key].text }}</el-text>
						<el-row v-if="statistics" class="statistics" justify="space-evenly">
							<el-col :xs="8" :sm="8" :md="24" :lg="24" :xl="24">
								<el-statistic title="Average" :value="statistics[key]?.average" />
							</el-col>
							<el-col :xs="8" :sm="8" :md="24" :lg="24" :xl="24">
								<el-statistic title="Minimum" :value="statistics[key]?.min" />
							</el-col>
							<el-col :xs="8" :sm="8" :md="24" :lg="24" :xl="24">
								<el-statistic title="Maximum" :value="statistics[key]?.max" />
							</el-col>
						</el-row>
					</el-col>
					<el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
						<el-row justify="space-evenly" class="filter">
							<el-alert v-if="invalidDate" title="Invalid date range: Please chose a date range which is under a month." />
							<el-date-picker v-model="filteredRange" type="datetimerange" start-placeholder="Start date" end-placeholder="End date" format="DD/MM/YY HH:mm" date-format="DD/MM/YY" time-format="HH:mm" value-format="YYYY-MM-DDTHH:mm:ssZ" />
							<el-button type="primary" @click="setFilter">
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M3.9 54.9C10.5 40.9 24.5 32 40 32l432 0c15.5 0 29.5 8.9 36.1 22.9s4.6 30.5-5.2 42.5L320 320.9 320 448c0 12.1-6.8 23.2-17.7 28.6s-23.8 4.3-33.5-3l-64-48c-8.1-6-12.8-15.5-12.8-25.6l0-79.1L9 97.3C-.7 85.4-2.8 68.8 3.9 54.9z"/></svg>
								Filter Data
							</el-button>
						</el-row>
						<line-chart v-if="activeTab === key" :sensorName="sensor.name" :dateRange="dateRange" :step="step" :measurement="key" :thresholdMin="sensor.thresholds[key][0]" :thresholdMax="sensor.thresholds[key][1]" ></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
		</el-tabs>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			activeTab: 'temperature',
			tabData: {
				soil_moisture: {
					label: 'Soil Moisture',
					text: 'Soil moisture is essential for plant growth, as it impacts water availability for uptake, nutrient transport, and root development. Proper soil moisture levels promote healthy plant growth, reduce stress, and optimize photosynthesis and nutrient absorption.',
				},
				soil_temperature: {
					label: 'Soil Temperature',
					text: 'Soil temperature plays a crucial role in plant growth as it directly affects root development, nutrient uptake, and microbial activity in the soil. Maintaining the right soil temperature ensures healthier plants, faster growth, and better resistance to stress.',
				},
				humidity: {
					label: 'Humidity',
					text: 'Humidity significantly affects plant transpiration, water balance, and disease resistance. Maintaining optimal humidity levels promotes efficient water use, prevents dehydration, and supports overall plant health.',
				},
				temperature: {
					label: 'Temperature',
					text: 'Temperature is a vital environmental factor that regulates plant metabolism, enzyme activity, and growth cycles. Ensuring optimal temperature conditions enhances plant resilience, flowering, and overall productivity.',
				},
				co2: {
					label: 'CO2',
					text: 'Carbon dioxide is a critical component of photosynthesis, driving energy production and growth. Elevated CO₂ levels within optimal ranges can boost photosynthetic efficiency, improve biomass, and enhance crop yields.',
				},
				barometric_pressure: {
					label: 'Barometric Pressure',
					text: 'Barometric pressure influences gas exchange, water movement, and plant transpiration rates. Stable atmospheric pressure supports efficient physiological processes, ensuring steady growth and development.',
				},
				light_intensity: {
					label: 'Light Intensity',
					text: 'Light intensity is a key factor in plant growth, directly influencing photosynthesis, energy production, and biomass accumulation. Adequate light intensity enhances plant vigor, accelerates development, and improves yield quality.',
				},
			},
			filteredRange: [moment().subtract(24, 'hours').toISOString(), moment().toISOString()],
			dateRange: [moment().subtract(24, 'hours').toISOString(), moment().toISOString()],
			step: 'hour',
			invalidDate: false,
			statistics: null,
		};
	},
	computed: {
		sensors() {
			return this.$stores.sensorStore.sensorsByMeasurement;
		},
	},
	methods: {
		setFilter() {
			this.invalidDate = false;
			this.dateRange = [this.filteredRange[0], this.filteredRange[1]];
			let duration = moment(this.dateRange[1]).diff(moment(this.dateRange[0]), 'minutes');

			if (duration <= 60) {
				this.step = 'minute';
			} else if (duration <= 1440) {
				this.step = 'hour';
			} else if (duration <= 43200) {
				this.step = 'day';
			} else {
				this.step = 'month';
			}
		},
	},
	mounted() {
		console.log('mounted')
		this.$stores.sensorStore.getStatistics()
		.then(data => this.statistics = data);
	},
};
</script>
<style lang="scss">
.data {
	.statistics {
		margin-top: 3em;
		.el-statistic {
			text-align: center;

			.el-statistic__head {
				font-size: 1em !important;
			}

			.el-statistic__number {
				font-size: 1.5em !important;
			}
		}
	}

	.el-col {
		padding-bottom: 2em;

		.el-button {
			margin-left: 12px;
		}
	}

	.filter {
		margin-bottom: 1em;
	}
}
</style>
