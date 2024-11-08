<template>
	<el-container>
		<el-header>
			<el-menu default-active="/" mode="horizontal" :ellipsis="false" router>
				<el-menu-item>
					<el-text size="large" tag="b">🍐 ioPear</el-text>
				</el-menu-item>
				<template v-if="!loading && Object.keys(plant).length">
					<el-menu-item index="/">Dashboard</el-menu-item>
					<el-menu-item index="/plants">Plants</el-menu-item>
					<el-menu-item index="/actions">Actions</el-menu-item>
					<el-menu-item index="/settings">Settings</el-menu-item>
				</template>
			</el-menu>
		</el-header>
		<el-main>
			<el-aside></el-aside>
			<el-text v-if="loading" class="loading" size="large">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
				Loading Data
			</el-text>
			<welcome-page v-else-if="!Object.keys(plant).length"></welcome-page>
			<router-view v-else></router-view>
		</el-main>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			activeIndex: 'dashboard',
			plant: null,
			config: null,
			loading: true,
		};
	},
	methods: {
		getData() {
			return Promise.allSettled([
				// this.getConfig(),//
				this.getPlant(),
			])
			.then((outcomes) => {
				if (outcomes.some(o => o.status === 'rejected')) {
					setTimeout(this.getData, 1000);
				}
				else {
					this.loading = false;
				}
			});
		},
		getPlant() {
			return axios.get('http://' + host + '/get_plant')
			.then(({data}) => {
				this.plant = data;
			});
		},
		// getConfig() {
		// 	return axios.get('http://' + host + '/get_config')
		// 	.then(({data}) => {
		// 		Object.assign(this.config, data);
		// 	});
		// },
	},
	mounted() {
		this.getData();
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

.loading {
	justify-content: center;
	margin-top: 2em;
}
</style>
