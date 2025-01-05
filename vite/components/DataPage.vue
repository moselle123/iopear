<template>
	<el-container class="data" direction="vertical">
		<el-text class="title">Data</el-text>
		<el-tabs v-model="activeTab">
			<el-tab-pane label="Soil Moisture" name="soil moisture">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Soil moisture is essential for plant growth, as it impacts water availability for uptake, nutrient transport, and root development. Proper soil moisture levels promote healthy plant growth, reduce stress, and optimize photosynthesis and nutrient absorption.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.SS" :dateRange="[startDate, endDate]" step="minute" measurement="soil_moisture"></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="Soil Temperature" name="soil temperature">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Soil temperature plays a crucial role in plant growth as it directly affects root development, nutrient uptake, and microbial activity in the soil. Maintaining the right soil temperature ensures healthier plants, faster growth, and better resistance to stress.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.SS" :dateRange="[startDate, endDate]" step="minute" measurement="soil_temperature"></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="Humidity" name="humidity">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Humidity significantly affects plant transpiration, water balance, and disease resistance. Maintaining optimal humidity levels promotes efficient water use, prevents dehydration, and supports overall plant health.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.SHT31" :dateRange="[startDate, endDate]" step="minute" measurement="humidity"></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="Air Temperature" name="air temperature">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Temperature is a vital environmental factor that regulates plant metabolism, enzyme activity, and growth cycles. Ensuring optimal temperature conditions enhances plant resilience, flowering, and overall productivity.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.SHT31" :dateRange="[startDate, endDate]" step="minute" measurement="temperature"></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="CO2" name="co2">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Carbon dioxide is a critical component of photosynthesis, driving energy production and growth. Elevated CO₂ levels within optimal ranges can boost photosynthetic efficiency, improve biomass, and enhance crop yields.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.SS" :dateRange="[startDate, endDate]" step="minute" measurement="soil_temperature"></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="Barometric Pressure" name="barometric pressure">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Barometric pressure influences gas exchange, water movement, and plant transpiration rates. Stable atmospheric pressure supports efficient physiological processes, ensuring steady growth and development.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.SS" :dateRange="[startDate, endDate]" step="minute" measurement="soil_temperature"></line-chart>
					</el-col>
				</el-row>
			</el-tab-pane>
			<el-tab-pane label="Light Intensity" name="light intensity">
				<el-row>
					<el-col :xs="24" :sm="7" :md="7" :lg="7" :xl="7">
						<el-text>Light intensity is a key factor in plant growth, directly influencing photosynthesis, energy production, and biomass accumulation. Adequate light intensity enhances plant vigor, accelerates development, and improves yield quality.</el-text>
					</el-col>
					<el-col :xs="24" :sm="16" :md="16" :lg="16" :xl="16">
						<line-chart :sensor="sensors.TSL2561" :dateRange="[startDate, endDate]" step="minute" measurement="lux"></line-chart>
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
			activeTab: 'soil moisture',
			startDate: moment().subtract(1, 'hours').toISOString(),
			endDate: moment().toISOString(),
		};
	},
	computed: {
		sensors() {
			return this.$stores.sensorStore.sensorsObj;
		},
	},
};
</script>
<style lang="scss" scoped>
.data {

}
</style>
