<template>
	<el-card class="notifications-card" >
		<template #header>
			<el-row justify="space-between">
				<el-text size="large">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M224 0c-17.7 0-32 14.3-32 32l0 19.2C119 66 64 130.6 64 208l0 18.8c0 47-17.3 92.4-48.5 127.6l-7.4 8.3c-8.4 9.4-10.4 22.9-5.3 34.4S19.4 416 32 416l384 0c12.6 0 24-7.4 29.2-18.9s3.1-25-5.3-34.4l-7.4-8.3C401.3 319.2 384 273.9 384 226.8l0-18.8c0-77.4-55-142-128-156.8L256 32c0-17.7-14.3-32-32-32zm45.3 493.3c12-12 18.7-28.3 18.7-45.3l-64 0-64 0c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7z"/></svg>
					Notifications
				</el-text>
				<svg @click="refreshNotifications" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M105.1 202.6c7.7-21.8 20.2-42.3 37.8-59.8c62.5-62.5 163.8-62.5 226.3 0L386.3 160 352 160c-17.7 0-32 14.3-32 32s14.3 32 32 32l111.5 0c0 0 0 0 0 0l.4 0c17.7 0 32-14.3 32-32l0-112c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 35.2L414.4 97.6c-87.5-87.5-229.3-87.5-316.8 0C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5zM39 289.3c-5 1.5-9.8 4.2-13.7 8.2c-4 4-6.7 8.8-8.1 14c-.3 1.2-.6 2.5-.8 3.8c-.3 1.7-.4 3.4-.4 5.1L16 432c0 17.7 14.3 32 32 32s32-14.3 32-32l0-35.1 17.6 17.5c0 0 0 0 0 0c87.5 87.4 229.3 87.4 316.7 0c24.4-24.4 42.1-53.1 52.9-83.8c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.5 62.5-163.8 62.5-226.3 0l-.1-.1L125.6 352l34.4 0c17.7 0 32-14.3 32-32s-14.3-32-32-32L48.4 288c-1.6 0-3.2 .1-4.8 .3s-3.1 .5-4.6 1z"/></svg>
			</el-row>
		</template>
		<el-text v-if="loading" size="large" class="loading">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
			Loading {{ title }} data
		</el-text>
		<el-container v-else direction="vertical">
			<el-row class="notification-settings" justify="space-between">
				<button @click="previousDay"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M41.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.3 256 246.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/></svg></button>
				<el-text>{{ days[currentDayIndex] }}</el-text>
				<button @click="nextDay"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"><path d="M278.6 233.4c12.5 12.5 12.5 32.8 0 45.3l-160 160c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L210.7 256 73.4 118.6c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0l160 160z"/></svg></button>
			</el-row>
			<el-timeline>
				<el-timeline-item v-for="notification in notifications[days[currentDayIndex]]" :key="notification" :timestamp="notification.timestamp" >
					<el-row align="middle">
						<el-tag effect="plain" :class="notification.notification_type === 'event' ? 'event' : 'action'">{{ notification.notification_type }}</el-tag>
						<el-text>{{ actionsAndEvents[notification.entity_id]?.name }}</el-text>
					</el-row>
				</el-timeline-item>
			</el-timeline>
		</el-container>
	</el-card>
</template>
<script>
export default {
	data() {
		return {
			loading: false,
			actionsAndEvents: null,
			notifications: null,
			currentDayIndex: 0,
			days: null,
		};
	},
	methods: {
		refreshNotifications() {
			this.loading = true;
			this.$stores.notificationStore.getNotifications()
			.then((data) => {
				this.notifications = data;
				this.loading = false;
			});
		},
		toggleNotifications() {
			this.isNotificationsVisible = ! this.isNotificationsVisible;
		},
		hideNotifications() {
			this.isNotificationsVisible = false;
		},
		nextDay() {
			this.currentDayIndex === this.days.length - 1 ? this.currentDayIndex = 0 : this.currentDayIndex++;
		},
		previousDay() {
			this.currentDayIndex === 0 ? this.currentDayIndex = this.days.length - 1 : this.currentDayIndex--;
		},
	},
	beforeMount() {
		this.notifications = this.$stores.notificationStore.notificationsObj;
		this.actionsAndEvents = Object.assign({}, this.$stores.eventStore.eventsObj, this.$stores.actionStore.actionsObj)
		this.days = Object.keys(this.notifications);
	},
};
</script>
<style lang="scss" scoped>
.notifications-card {
	position: absolute;

	top: 60px;
	right: 1em;
	width: 80%;
	max-width: 350px;
	height: 60vh;
	max-height: 500px;

	z-index: 1000;

	.notification-settings {
		button {
			width: auto;

			border: 0;
			background-color: transparent;
		}
	}

	.el-timeline {
		max-height: 500px;
		padding: 1em;

		overflow-y: scroll;

		.el-timeline-item__content {
			padding: 0.5em 0;

			.el-row {
				.el-tag {
					margin: 0 0.5em 0 0;

					text-transform: capitalize;
				}
			}
		}
	}
}
</style>
