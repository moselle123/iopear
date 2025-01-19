<template>
	<el-container direction="vertical" class="configure-events">
		<el-text>Create an event to register when a sensor goes above or below a set value.</el-text>
		<el-row class="page-header">
			<el-alert v-if="newEvents.length" type="warning" title="Please save changes before moving on." />
			<el-button type="primary" @click="addEvent">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 144L48 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l144 0 0 144c0 17.7 14.3 32 32 32s32-14.3 32-32l0-144 144 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-144 0 0-144z"/></svg>
				Create Event
			</el-button>
		</el-row>
		<el-text v-if=" ! (events.length || newEvents.length)" class="no-content">No Events to Display</el-text>
		<el-card v-else>
			<el-collapse accordion>
				<el-collapse-item v-for="(event, index) in displayedEvents" :key="index" :title="event._id ? labels.measurements[event.measurement] + ' ' + labels[event.condition] + ' ' + event.threshold : 'New Event'" :name="index">
					<el-form label-position="top">
						<el-form-item label="Enabled">
							<el-switch v-model="event.is_enabled" />
						</el-form-item>
						<el-form-item label="Measurement">
							<el-select v-model="event.measurement">
								<el-option v-for="(label, measurement) in labels.measurements" :key="label" :label="label" :value="measurement" />
							</el-select>
						</el-form-item>
						<el-form-item label="Condition">
							<el-select v-model="event.condition">
								<el-option label="Greater Than" value="greater_than" />
								<el-option label="Less Than" value="less_than" />
							</el-select>
						</el-form-item>
						<el-form-item label="Threshold">
							<el-input v-model="event.threshold" type="number" inputmode="tel" />
						</el-form-item>
					</el-form>
					<el-row justify="end">
						<el-button type="primary" v-if="event?._id" @click="deleteEvent(event)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-242.7c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32L64 32zm0 96c0-17.7 14.3-32 32-32l192 0c17.7 0 32 14.3 32 32l0 64c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-64zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
							Delete Event
						</el-button>
						<el-button type="primary" @click="saveChanges(event)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-242.7c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32L64 32zm0 96c0-17.7 14.3-32 32-32l192 0c17.7 0 32 14.3 32 32l0 64c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-64zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
							Save Changes
						</el-button>
					</el-row>
				</el-collapse-item>
			</el-collapse>
		</el-card>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
			newEvents: [],
		};
	},
	computed: {
		events() {
			return this.$stores.eventStore.eventsArr;
		},
		sensors() {
			return this.$stores.sensorStore.sensorsByMeasurement;
		},
		displayedEvents() {
			return this.events.concat(this.newEvents);
		},
		labels() {
			return {
				measurements: {
					soil_moisture: 'Soil Moisture',
					soil_temperature: 'Soil Temperature',
					humidity: 'Humidity',
					temperature: 'Temperature',
					light_intensity: 'Light Intensity',
					barometric_pressure: 'Barometric Pressure',
					co2: 'CO2',
				},
				greater_than: 'Greater Than',
				less_than: 'Less Than',
			};
		},
		notificationName() {
			return
		},
	},
	methods: {
		addEvent() {
			this.newEvents.push({
				is_enabled: true,
				measurement: null,
				condition: null,
			});
		},
		saveChanges(event, index) {
			event?._id ? this.updateEvent(event) : this.createEvent(event, index);
		},
		createEvent(event, index) {
			event.sensor_id = this.sensors[event.measurement]._id;
			event.threshold = Number(event.threshold);
			this.$stores.eventStore.createEvent(event)
			.then(() => this.newEvents.splice(index, 1));
		},
		updateEvent(event) {
			this.$stores.eventStore.updateEvent(event);
		},
		deleteEvent(event) {
			this.$stores.eventStore.deleteEvent(event);
		},
	},
	mounted() {
		this.$stores.eventStore.getEvents();
	},
};
</script>
<style lang="scss" scoped>
.configure-events {

}
</style>
