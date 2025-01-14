<template>
	<el-container class="data" direction="vertical">
		<el-text class="title">Data</el-text>
		<el-tabs v-model="activeTab">
			<el-tab-pane v-for="(sensor, key) in sensors" :key="key" :label="tabData[key].label" :name="key">
				<el-row justify="space-between">
					<el-col :xs="24" :sm="24" :md="7" :lg="7" :xl="7">
						<el-text>{{ tabData[key].text }}</el-text>
					</el-col>
					<el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
						<el-row justify="space-evenly" class="filter">
							<el-alert v-if="invalidDate" title="Invalid date range: Please chose a date range which is under a month." />
							<el-date-picker v-model="filteredRange" type="datetimerange" start-placeholder="Start date" end-placeholder="End date" format="DD/MM/YY HH:mm" date-format="DD/MM/YY" time-format="HH:mm" value-format="YYYY-MM-DDTHH:mm:ssZ" />
							<el-button @click="setFilter">Filter Data</el-button>
						</el-row>
						<line-chart v-if="activeTab === key" :sensorName="sensor.name" :dateRange="dateRange" :step="step" :measurement="key"></line-chart>
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
			activeTab: 'soil_moisture',
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
		}
	},
};
</script>
<style lang="scss" scoped>
.data {
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
