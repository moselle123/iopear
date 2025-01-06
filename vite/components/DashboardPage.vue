<template>
	<el-container class="dashboard" direction="vertical" >
		<el-row justify="space-between">
			<!-- <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16"> -->
				<el-container class="left-column" direction="vertical">
					<el-text class="title">{{ plant?.name }}</el-text>
					<el-text>{{ plantType?.description }}</el-text>
					<el-row justify="space-between">
						<el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
							<line-chart sensorName="SHT31" :dateRange="[startDate, endDate]" step="minute" measurement="temperature"></line-chart>
						</el-col>
						<el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
							<line-chart sensorName="SHT31" :dateRange="[startDate, endDate]" step="minute" measurement="humidity"></line-chart>
						</el-col>
						<el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
							<line-chart sensorName="SS" :dateRange="[startDate, endDate]" step="minute" measurement="soil moisture"></line-chart>
						</el-col>
						<el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
							<line-chart sensorName="SS" :dateRange="[startDate, endDate]" step="minute" measurement="soil temperature"></line-chart>
						</el-col>
						<el-col :xs="24" :sm="12" :md="8" :lg="8" :xl="8">
							<line-chart sensorName="TSL2561" :dateRange="[startDate, endDate]" step="minute" measurement="light intensity"></line-chart>
						</el-col>
					</el-row>
				</el-container>
			<!-- </el-col> -->
			<!-- <el-col :xs="24" :sm="24" :md="7" :lg="7" :xl="7">
				<el-card>
					<template #header>
						<el-text>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M224 0c-17.7 0-32 14.3-32 32l0 19.2C119 66 64 130.6 64 208l0 25.4c0 45.4-15.5 89.5-43.8 124.9L5.3 377c-5.8 7.2-6.9 17.1-2.9 25.4S14.8 416 24 416l400 0c9.2 0 17.6-5.3 21.6-13.6s2.9-18.2-2.9-25.4l-14.9-18.6C399.5 322.9 384 278.8 384 233.4l0-25.4c0-77.4-55-142-128-156.8L256 32c0-17.7-14.3-32-32-32zm0 96c61.9 0 112 50.1 112 112l0 25.4c0 47.9 13.9 94.6 39.7 134.6L72.3 368C98.1 328 112 281.3 112 233.4l0-25.4c0-61.9 50.1-112 112-112zm64 352l-64 0-64 0c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7s18.7-28.3 18.7-45.3z"/></svg>
							Notifications
						</el-text>
					</template>
				</el-card>
			</el-col> -->
		</el-row>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			startDate: moment().subtract(1, 'hours').toISOString(),
			endDate: moment().toISOString(),
		};
	},
	computed: {
		plant() {
			return this.$stores.plantStore.plantData;
		},
		plantType() {
			return this.$stores.plantStore.plantTypeData;
		},
	},
};
</script>
<style lang="scss" scoped>
.left-column {
	gap: 1em;
}
</style>
