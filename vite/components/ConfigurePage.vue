<template>
	<el-container class="configure" direction="vertical" >
		<el-text class="title">Configure</el-text>
		<el-tabs v-model="activeTab">
			<el-tab-pane label="Actions" name="actions">
				<el-collapse accordion>
					<el-collapse-item v-for="(action, index) in actions" :key="index" :title="action.name" :name="index">
						<template #header>
							<el-text>{{ action.name }}</el-text>
						</template>
					</el-collapse-item>
				</el-collapse>
			</el-tab-pane>
			<el-tab-pane label="Events" name="events">
				<el-collapse accordion>
					<el-collapse-item v-for="(event, index) in events" :key="index" :title="event.name" :name="index">
						<template #header>
							<el-text>{{ event.name }}</el-text>
						</template>
					</el-collapse-item>
				</el-collapse>
			</el-tab-pane>
			<el-tab-pane label="Sensors" name="sensors">
				<el-collapse accordion>
					<el-collapse-item v-for="(sensor, index) in sensors" :key="index" :title="sensor.name" :name="index">
						<template #header>
							<el-text>{{ sensor.name }}</el-text>
						</template>
					</el-collapse-item>
				</el-collapse>
			</el-tab-pane>
		</el-tabs>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			activeTab: 'actions',
			actions: [
				{
					name: 'Turn on water pump',
				},
				{
					name: 'Turn off water pump',
				},
			],
			events: [
				{
					name: 'Temperature too high',
				},
				{
					name: 'Temperature too low',
				},

			],
			sensors: [
				{
					name: 'Soil Moisture Sensor',
				},
				{
					name: 'Humidity Sensor',
				},

			],
		};
	},
};
</script>
<style lang="scss" scoped>
.configure {

}
</style>
