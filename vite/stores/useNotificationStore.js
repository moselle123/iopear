import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
	state: () => ({
		notifications: {},
	}),
	getters: {
		notificationsObj() {
			return this.notifications;
		},
	},
	actions: {
		getNotifications() {
			let now = new Date();
			let lastWeek = new Date();
			lastWeek.setDate(now.getDate() - 7);
			return axios.get(host + '/get_notifications', { params: { start_date: lastWeek, end_date: now } })
			.then(({data}) => {
				data.forEach(notification => {
					let date = moment(notification.timestamp);
					let formattedDate;

					if (date.isSame(now, 'day')) {
						formattedDate = "Today";
					} else if (date.isSame(moment().subtract(1, 'days'), 'day')) {
						formattedDate = "Yesterday";
					} else {
						formattedDate = date.format('dddd');
					}

					if (! this.notifications[formattedDate]) {
						this.notifications[formattedDate] = [];
					}
					this.notifications[formattedDate].push(notification);
				});

				return this.notifications;
			});
		},
	},
});