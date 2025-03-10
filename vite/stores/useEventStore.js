import { defineStore } from 'pinia';

export const useEventStore = defineStore('event', {
	state: () => ({
		events: [],
	}),
	getters: {
		eventsArr() {
			return this.events;
		},
		eventsObj() {
			let obj = {}
			this.events.forEach((event) => {
				obj[event._id] = {}
				Object.assign(obj[event._id], event);
				delete obj[event._id]._id;
			})
			return obj;
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
			return axios.put(host + '/update_event/' + event._id, {"name": event.name, "measurement": event.measurement, "conditions": event.conditions, "scheduled_time": event.scheduled_time, "actions": event.actions, "logic": event.logic, "is_enabled": event.is_enabled})
			.then(() => this.getEvents());
		},
		deleteEvent(event) {
			return axios.delete(host + '/delete_event/' + event._id)
			.then(() => this.getEvents());
		},
	},
});