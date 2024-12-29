<template>
	<el-container class="data" direction="vertical">
		<el-text class="title">Data</el-text>
		<el-tabs v-model="activeTab">
			<el-tab-pane label="Soil Moisture" name="soil moisture">

			</el-tab-pane>
			<el-tab-pane label="Soil Temperature" name="soil temperature">

			</el-tab-pane>
			<el-tab-pane label="Humidity" name="humidity">

			</el-tab-pane>
			<el-tab-pane label="Air Temperature" name="air temperature">

			</el-tab-pane>
			<el-tab-pane label="CO2" name="co2">

			</el-tab-pane>
			<el-tab-pane label="Barometric Pressure" name="barometric pressure">

			</el-tab-pane>
			<el-tab-pane label="Light Intensity" name="light intensity">

			</el-tab-pane>
		</el-tabs>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			activeTab: 'soil moisture',
		};
	},
};
</script>
<style lang="scss" scoped>

</style>
