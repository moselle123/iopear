<template>
	<el-container class="dashboard" direction="vertical" >
		<el-text class="title">{{ plant?.name }}</el-text>
		<el-text>{{ plantType?.description }}</el-text>
		<el-row class="grid" justify="space-between">
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
		sensors() {
			return this.$stores.sensorStore.sensorsByMeasurement;
		},
	},
};
</script>
<style lang="scss" scoped>
.dashboard {
	gap: 1em;
}
</style>
