<template>
	<el-card class="notifications-card" >
		<template #header>
			<el-row justify="space-between">
				<el-text size="large">Notifications</el-text>
			</el-row>
		</template>
		<el-text v-if="loading" size="large" class="loading">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
			Loading {{ title }} data
		</el-text>
		<el-container v-else-if="Object.keys(notifications).length" direction="vertical">
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
		<el-text v-else class="no-content">No Notifications to Display</el-text>
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
	max-width: 380px;
	height: 60vh;
	max-height: 500px;
	margin-top: 1em;

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
		height: 80%;
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
