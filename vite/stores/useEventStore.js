import { defineStore } from 'pinia';

export const useEventStore = defineStore('event', {
	state: () => ({
		events: [],
	}),
	getters: {
		eventsArr() {
			return this.events;
		},
	},
	actions: {
		getEvents() {
			return axios.get(host + '/get_events')
			.then(({data}) => {
				this.events = data;
			});
		},
		createEvent(event) {
			return axios.post(host + '/create_event', event)
			.then(() => this.getEvents());
		},
		updateEvent(event) {
			return axios.put(host + '/update_event/' + event._id, event)
			.then(() => this.getEvents());
		},
		deleteEvent(event) {
			return axios.delete(host + '/delete_event/' + event._id)
			.then(() => this.getEvents());
		},
		getEventInstances(startDate, endDate) {
			return axios.get(host + '/get_event_instances', { params: { start_date: startDate, end_date: endDate } })
			.then(({data}) => data);
		},
	}
});