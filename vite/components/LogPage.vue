<template>
	<el-container class="log" direction="vertical" >
		<el-row justify="end" class="filter">
			<el-alert v-if="invalidDate" title="Invalid date range: Please chose a date range which is under a month." />
			<el-date-picker v-model="filteredRange" type="datetimerange" start-placeholder="Start date" end-placeholder="End date" format="DD/MM/YY HH:mm" date-format="DD/MM/YY" time-format="HH:mm" value-format="YYYY-MM-DDTHH:mm:ssZ" />
			<el-button type="primary" @click="setFilter">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M3.9 54.9C10.5 40.9 24.5 32 40 32l432 0c15.5 0 29.5 8.9 36.1 22.9s4.6 30.5-5.2 42.5L320 320.9 320 448c0 12.1-6.8 23.2-17.7 28.6s-23.8 4.3-33.5-3l-64-48c-8.1-6-12.8-15.5-12.8-25.6l0-79.1L9 97.3C-.7 85.4-2.8 68.8 3.9 54.9z"/></svg>
				Filter Notifications
			</el-button>
		</el-row>
		<el-text v-if=" ! Object.keys(notifications).length" class="no-content">No system events have been logged for the selected time frame.</el-text>
		<el-card v-else class="timeline" >
			<template #header>
				<el-text size="large">
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M224 0c-17.7 0-32 14.3-32 32l0 19.2C119 66 64 130.6 64 208l0 18.8c0 47-17.3 92.4-48.5 127.6l-7.4 8.3c-8.4 9.4-10.4 22.9-5.3 34.4S19.4 416 32 416l384 0c12.6 0 24-7.4 29.2-18.9s3.1-25-5.3-34.4l-7.4-8.3C401.3 319.2 384 273.9 384 226.8l0-18.8c0-77.4-55-142-128-156.8L256 32c0-17.7-14.3-32-32-32zm45.3 493.3c12-12 18.7-28.3 18.7-45.3l-64 0-64 0c0 17 6.7 33.3 18.7 45.3s28.3 18.7 45.3 18.7s33.3-6.7 45.3-18.7z"/></svg>
					Notifications
				</el-text>
			</template>
			<el-timeline>
				<el-timeline-item v-for="notification in notifications" :key="notification" :timestamp="notification.timestamp" >
					<el-text>{{ entities[notification.entity_id].name }}</el-text>
					<el-tag effect="plain" :class="notification.notification_type === 'event' ? 'event' : 'action'">{{ notification.notification_type }}</el-tag>
				</el-timeline-item>
			</el-timeline>
		</el-card>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			filteredRange: [moment().subtract(24, 'hours').toISOString(), moment().toISOString()],
			dateRange: [moment().subtract(24, 'hours').toISOString(), moment().toISOString()],
			notifications: {},
			invalidDate: false,
			entities: null,
		};
	},
	methods: {
		getNotifications() {
			this.$stores.notificationStore.getNotifications(this.dateRange[0], this.dateRange[1])
			.then((data) => {
				this.notifications = data;
			});
		},
		setFilter() {
			this.invalidDate = false;
			this.dateRange = [this.filteredRange[0], this.filteredRange[1]];
			let duration = moment(this.dateRange[1]).diff(moment(this.dateRange[0]), 'minutes');


			this.getNotifications();
		},
	},
	mounted() {
		this.entities = Object.assign({}, this.$stores.eventStore.eventsObj, this.$stores.actionStore.actionsObj);
		this.$stores.notificationStore.getNotifications(this.dateRange[0], this.dateRange[1])
		.then((data) => {
			this.notifications = data;
		});
	},
};
</script>
<style lang="scss" scoped>
.log {
	height: 100%;

	.filter {
		gap: 1em;
		margin-bottom: 1em;

		.el-button {
			width: 10.5em !important;
		}
	}

	.el-card {
		height: 80vh;
	}

	.el-timeline {
		margin: 1em 0;

		.el-tag {
			margin: 1em 0;

			text-transform: capitalize;
		}
	}
}
</style>
