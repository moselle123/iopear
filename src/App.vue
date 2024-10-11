<template>
	<el-container>
		<el-header>
			<el-menu default-active="/" mode="horizontal" :ellipsis="false" router>
				<el-menu-item>
					<el-text size="large" tag="b">🍐 ioPear</el-text>
				</el-menu-item>
				<el-menu-item index="/">Dashboard</el-menu-item>
				<el-menu-item index="/plants">Plants</el-menu-item>
				<el-menu-item index="/actions">Actions</el-menu-item>
				<el-menu-item index="/settings">Settings</el-menu-item>
			</el-menu>
		</el-header>
		<el-main>
			<el-aside></el-aside>
			<router-view></router-view>
		</el-main>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			activeIndex: 'dashboard',
		};
	},
};
</script>
<style lang="scss" scoped>
.el-header {
	padding: 0;
	
	.el-menu-item {
		&:first-child {
			margin-right: auto;
		}
	}
}
</style>
