<template>
	<el-container class="configure" direction="vertical" >
		<el-text class="title">Configure</el-text>
		<el-tabs v-model="activeTab">
			<el-tab-pane label="Events" name="events">
				<events-configuration v-if="activeTab === 'events'" />
			</el-tab-pane>
			<el-tab-pane label="Actions" name="actions">
				<actions-configuration v-if="activeTab === 'actions'" />
			</el-tab-pane>
			<el-tab-pane label="Sensors" name="sensors">
				<sensors-configuration />
			</el-tab-pane>
		</el-tabs>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			activeTab: 'events',
		};
	},
};
</script>
<style lang="scss" scoped>
.configure {

}
</style>
