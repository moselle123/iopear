import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
        state: () => ({
                notifications: [],
        }),
        getters: {
                notificationsArr() {
                        return this.notifications;
                },
        },
        actions: {
		getNotifications(startDate, endDate) {
			return axios.get(host + '/get_notifications', { params: { start_date: startDate, end_date: endDate } })
			.then(({data}) => data);
		},
        },
});