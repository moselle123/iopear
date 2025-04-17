<template>
	<el-container class="app-wrapper">
		<Transition name="slide-fade">
			<el-aside v-if="!hideNav">
				<el-row class="aside-header" justify="space-between">
					<el-text class="title">🌵 ioPear</el-text>
					<svg @click="toggleNav" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="M342.6 150.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L192 210.7 86.6 105.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L146.7 256 41.4 361.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L192 301.3 297.4 406.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L237.3 256 342.6 150.6z"/></svg>
				</el-row>
				<el-menu :default-active="$router.path" :ellipsis="false" router >
					<el-menu-item index="/" route="/" @click="closeNav">
						<el-text>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M272 96c-78.6 0-145.1 51.5-167.7 122.5c33.6-17 71.5-26.5 111.7-26.5l88 0c8.8 0 16 7.2 16 16s-7.2 16-16 16l-16 0-72 0s0 0 0 0c-16.6 0-32.7 1.9-48.3 5.4c-25.9 5.9-49.9 16.4-71.4 30.7c0 0 0 0 0 0C38.3 298.8 0 364.9 0 440l0 16c0 13.3 10.7 24 24 24s24-10.7 24-24l0-16c0-48.7 20.7-92.5 53.8-123.2C121.6 392.3 190.3 448 272 448l1 0c132.1-.7 239-130.9 239-291.4c0-42.6-7.5-83.1-21.1-119.6c-2.6-6.9-12.7-6.6-16.2-.1C455.9 72.1 418.7 96 376 96L272 96z"/></svg>
							Dashboard
						</el-text>
					</el-menu-item>
					<template v-if="!loading && Object.keys(plant).length">
						<el-menu-item index="/events" route="/events" @click="closeNav">
							<el-text>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M128 0c17.7 0 32 14.3 32 32l0 32 128 0 0-32c0-17.7 14.3-32 32-32s32 14.3 32 32l0 32 48 0c26.5 0 48 21.5 48 48l0 48L0 160l0-48C0 85.5 21.5 64 48 64l48 0 0-32c0-17.7 14.3-32 32-32zM0 192l448 0 0 272c0 26.5-21.5 48-48 48L48 512c-26.5 0-48-21.5-48-48L0 192zm64 80l0 32c0 8.8 7.2 16 16 16l32 0c8.8 0 16-7.2 16-16l0-32c0-8.8-7.2-16-16-16l-32 0c-8.8 0-16 7.2-16 16zm128 0l0 32c0 8.8 7.2 16 16 16l32 0c8.8 0 16-7.2 16-16l0-32c0-8.8-7.2-16-16-16l-32 0c-8.8 0-16 7.2-16 16zm144-16c-8.8 0-16 7.2-16 16l0 32c0 8.8 7.2 16 16 16l32 0c8.8 0 16-7.2 16-16l0-32c0-8.8-7.2-16-16-16l-32 0zM64 400l0 32c0 8.8 7.2 16 16 16l32 0c8.8 0 16-7.2 16-16l0-32c0-8.8-7.2-16-16-16l-32 0c-8.8 0-16 7.2-16 16zm144-16c-8.8 0-16 7.2-16 16l0 32c0 8.8 7.2 16 16 16l32 0c8.8 0 16-7.2 16-16l0-32c0-8.8-7.2-16-16-16l-32 0zm112 16l0 32c0 8.8 7.2 16 16 16l32 0c8.8 0 16-7.2 16-16l0-32c0-8.8-7.2-16-16-16l-32 0c-8.8 0-16 7.2-16 16z"/></svg>
								Events
							</el-text>
						</el-menu-item>
						<el-menu-item index="/sensors" route="/sensors" @click="closeNav">
							<el-text>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M160 64c-26.5 0-48 21.5-48 48l0 164.5c0 17.3-7.1 31.9-15.3 42.5C86.2 332.6 80 349.5 80 368c0 44.2 35.8 80 80 80s80-35.8 80-80c0-18.5-6.2-35.4-16.7-48.9c-8.2-10.6-15.3-25.2-15.3-42.5L208 112c0-26.5-21.5-48-48-48zM48 112C48 50.2 98.1 0 160 0s112 50.1 112 112l0 164.4c0 .1 .1 .3 .2 .6c.2 .6 .8 1.6 1.7 2.8c18.9 24.4 30.1 55 30.1 88.1c0 79.5-64.5 144-144 144S16 447.5 16 368c0-33.2 11.2-63.8 30.1-88.1c.9-1.2 1.5-2.2 1.7-2.8c.1-.3 .2-.5 .2-.6L48 112zM208 368c0 26.5-21.5 48-48 48s-48-21.5-48-48c0-20.9 13.4-38.7 32-45.3L144 144c0-8.8 7.2-16 16-16s16 7.2 16 16l0 178.7c18.6 6.6 32 24.4 32 45.3z"/></svg>
								Sensors
							</el-text>
						</el-menu-item>
						<el-menu-item index="/data" route="/data" @click="closeNav">
							<el-text>
								<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M64 64c0-17.7-14.3-32-32-32S0 46.3 0 64L0 400c0 44.2 35.8 80 80 80l400 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L80 416c-8.8 0-16-7.2-16-16L64 64zm406.6 86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L320 210.7l-57.4-57.4c-12.5-12.5-32.8-12.5-45.3 0l-112 112c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L240 221.3l57.4 57.4c12.5 12.5 32.8 12.5 45.3 0l128-128z"/></svg>
								Data
							</el-text>
						</el-menu-item>
					</template>
				</el-menu>
			</el-aside>
		</Transition>
		<el-container :style="hideNav ? '' : {opacity: 0.7}">
			<el-header>
				<svg @click="toggleNav" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M0 96C0 78.3 14.3 64 32 64l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 128C14.3 128 0 113.7 0 96zM0 256c0-17.7 14.3-32 32-32l384 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 288c-17.7 0-32-14.3-32-32zM448 416c0 17.7-14.3 32-32 32L32 448c-17.7 0-32-14.3-32-32s14.3-32 32-32l384 0c17.7 0 32 14.3 32 32z"/></svg>
				<el-text class="title">🌵 ioPear</el-text>
				<svg v-if="isNotificationsVisible"  class="notification-bell" @click="toggleNotifications" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M224 0c-17.7 0-32 14.3-32 32l0 19.2C119 66 64 130.6 64 208l0 18.8c0 47-17.3 92.4-48.5 127.6l-7.4 8.3c-8.4 9.4-10.4 22.9-5.3 34.4S19.4 416 32 416l384 0c12.6 0 24-7.4 29.2-18.9s3.1-25-5.3-34.4l-7.4-8.3C401.3 319.2 384 273.9 384 226.8l0-18.8c0-77.4-55-142-128-156.8L256 32c0-17.7-14.3-32-32-32zm45.3 493.3c12-12 18.7-28.3 18.7-45.3l-64 0-64 0c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7z"/></svg>
				<svg v-else class="notification-bell" @click="toggleNotifications" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M224 0c-17.7 0-32 14.3-32 32l0 19.2C119 66 64 130.6 64 208l0 25.4c0 45.4-15.5 89.5-43.8 124.9L5.3 377c-5.8 7.2-6.9 17.1-2.9 25.4S14.8 416 24 416l400 0c9.2 0 17.6-5.3 21.6-13.6s2.9-18.2-2.9-25.4l-14.9-18.6C399.5 322.9 384 278.8 384 233.4l0-25.4c0-77.4-55-142-128-156.8L256 32c0-17.7-14.3-32-32-32zm0 96c61.9 0 112 50.1 112 112l0 25.4c0 47.9 13.9 94.6 39.7 134.6L72.3 368C98.1 328 112 281.3 112 233.4l0-25.4c0-61.9 50.1-112 112-112zm64 352l-64 0-64 0c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7s18.7-28.3 18.7-45.3z"/></svg>
				<notifications-popup v-if="isNotificationsVisible" />
			</el-header>
			<el-main @click="hidePopups">
				<welcome-page v-if=" !loading && ! Object.keys(plant).length" @setupComplete="$stores.plantStore.getPlant"></welcome-page>
				<router-view v-if=" ! loading && Object.keys(plant).length"></router-view>
			</el-main>
		</el-container>
		<el-dialog v-model="isModalVisible" width="500" :show-close="false">
			<el-text class="loading" size="large">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
				{{ loading ? 'Loading Data' : 'Reconnecting to ioPear'}}
			</el-text>
		</el-dialog>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			config: null,
			loading: true,
			hideNav: true,
			isNotificationsVisible: false,
			isWsConnected: false,
			isModalVisible: true,
		};
	},
	computed: {
		plant() {
			return this.$stores.plantStore.plantData;
		},
	},
	methods: {
		getData() {
			return Promise.allSettled([
				this.$stores.plantStore.getPlant(),
				this.$stores.sensorStore.getSensors(),
				this.$stores.eventStore.getEvents(),
				this.$stores.actionStore.getActions(),
				this.$stores.actuatorStore.getActuators(),
				this.$stores.notificationStore.getNotifications(),
			])
			.then((outcomes) => {
				if (outcomes.some(o => o.status === 'rejected')) {
					console.debug(outcomes);
				}
				else {
					this.loading = false;
					this.isModalVisible = false;
				}
			});
		},
		hidePopups() {
			this.closeNav();
			this.hideNotifications();
		},
		toggleNav() {
			this.hideNav = !this.hideNav;
			this.isNotificationsVisible = false;
		},
		closeNav() {
			this.hideNav = true;
		},
		toggleNotifications() {
			this.isNotificationsVisible = ! this.isNotificationsVisible;
		},
		hideNotifications() {
			this.isNotificationsVisible = false;
		},
	},
	mounted() {
		this.getData()
		.then(() => this.actionsAndEvents = Object.assign({}, this.$stores.eventStore.eventsObj, this.$stores.actionStore.actionsObj));

		socket.on("connect", () => {
			console.debug('websocket connected');
			this.isWsConnected = true;
			this.isModalVisible = false;
		});
		socket.on("disconnect", () => {
			console.debug('websocket disconnected');
			this.isWsConnected = false;
			this.isModalVisible = true;
		});
		socket.on("actuator-update", (data) => {
			console.debug('actuator update', data);
			this.$stores.actuatorStore.updateActuatorState(data);
		});
		socket.on("notification-update", () => {
			console.debug('notification-update');
			this.$stores.notificationStore.getNotifications();
		});
	},
};
</script>
<style lang="scss" scoped>
.app-wrapper {
	height: 100%;

	.slide-fade-enter-active , .slide-fade-leave-active {
		transition: all 0.3s ease-in-out;
	}

	.slide-fade-enter-from,
	.slide-fade-leave-to {
		transform: translateX(-300px);
	}

	.notification-bell {
		margin: 0 1em 0 auto;

		cursor: pointer;

		&:hover {
			path {
				fill-opacity: 0.8;
			}
		}
	}
}
</style>
