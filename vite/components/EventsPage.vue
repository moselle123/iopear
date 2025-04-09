<template>
	<el-container direction="vertical" class="events">
		<el-text class="title">Events</el-text>
		<el-text>Create new events or edit existing ones. Events can be triggered either at a scheduled time or based on specific sensor conditions. Each event can include one or more actions that will execute when its trigger conditions are met.</el-text>
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
				<el-collapse-item v-for="(event, index) in displayedEvents" :key="index" :name="index">
					<template #title>
						<el-tag v-if="event.is_threshold_event">Threshold</el-tag>
						<el-tag v-if=" ! event.is_enabled" type="danger">Disabled</el-tag>
						<el-text>{{ event._id ? event.name : 'New Event' }}</el-text>
					</template>
					<el-alert v-if="event.is_threshold_event" type="warning" title="Threshold events are auto-generated from sensor limits. They can't be deleted, but you can add actions or disable notifications." />
					<el-form label-position="top">
						<el-row class="grid" justify="space-evenly">
							<el-col :xs="24" :sm="24" :md="11" :lg="11" :xl="11">
								<el-form-item label="Name">
									<el-input v-model="event.name" :disabled="event.is_threshold_event" placeholder="Describe this event" />
								</el-form-item>
							</el-col>
							<el-col v-if=" ! event.is_threshold_event" :xs="24" :sm="24" :md="11" :lg="11" :xl="11">
								<el-form-item label="Schedule Event Time">
									<el-time-picker v-model="event.scheduled_time" arrow-control placeholder="When will the event trigger" clearable value-format="HH:mm" />
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="24" :md="11" :lg="11" :xl="11">
								<el-form-item label="Enable Event">
									<el-switch v-model="event.is_enabled" />
								</el-form-item>
							</el-col>
							<el-col v-if=" ! event.is_threshold_event" :xs="24" :sm="24" :md="11" :lg="11" :xl="11">
								<el-form-item label="Event Logic">
									<el-switch v-model="event.logic" active-text="Meet All Conditions" active-value="AND" inactive-text="Meet At Least 1 Condition" inactive-value="OR" />
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="24" :md="11" :lg="11" :xl="11">
								<el-form-item label="Conditions" class="complex-form-item">
									<el-text v-if=" ! Object.keys(event.conditions).length" class="no-content">Assign a condition which will be used to determine if this event is triggered.</el-text>
									<template v-else>
										<el-input v-for="(condition, index) in event.conditions" :key="condition" v-model="condition.value" placeholder="Value" type="number" inputmode="tel" >
											<template #prepend>
												<el-select v-model="condition.measurement" placeholder="Measurement" style="width: 50%">
													<el-option v-for="(label, measurement) in labels.measurements" :key="label" :label="label" :value="measurement" />
												</el-select>
												<el-select v-model="condition.type" placeholder="Condition" style="width: 50%">
													<el-option label="Greater Than" value="greater_than" />
													<el-option label="Less Than" value="less_than" />
												</el-select>
											</template>
											<template #append>
												<el-button @click="deleteCondition(event, index)"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg></el-button>
											</template>
										</el-input>
									</template>
									<el-row v-if=" ! event.is_threshold_event" justify="end">
										<el-button @click="addCondition(event)">
											<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 144L48 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l144 0 0 144c0 17.7 14.3 32 32 32s32-14.3 32-32l0-144 144 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-144 0 0-144z"/></svg>
											Add Condition
										</el-button>
									</el-row>
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="24" :md="11" :lg="11" :xl="11">
								<el-form-item label="Actions" class="complex-form-item">
									<el-text v-if=" ! Object.keys(event.actions).length" class="no-content">No actions are assigned to this event.</el-text>
									<template v-else>
										<el-row v-for="(actionId, index) in event.actions" :key="actionId" class="select-with-button">
											<el-select v-model="event.actions[index]">
												<el-option v-for="action in actions" :key="action" :label="action.name" :value="action._id" />
											</el-select>
											<el-button @click="deleteAction(event, index)"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg></el-button>
										</el-row>
									</template>
									<el-button @click="addAction(event)">
										<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 144L48 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l144 0 0 144c0 17.7 14.3 32 32 32s32-14.3 32-32l0-144 144 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-144 0 0-144z"/></svg>
										Add Action
									</el-button>
								</el-form-item>
							</el-col>
						</el-row>
					</el-form>
					<el-divider />
					<el-row justify="end">
						<el-button type="primary" v-if="event?._id && ! event.is_threshold_event" @click="deleteEvent(event)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg>
							Delete Event
						</el-button>
						<el-button type="primary" @click="saveChanges(event)">
							<svg v-if="currentlySaving === event._id" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
							<svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-242.7c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32L64 32zm0 96c0-17.7 14.3-32 32-32l192 0c17.7 0 32 14.3 32 32l0 64c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-64zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
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
			events: [],
			newEvents: [],
			labels: {
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
			},
			currentlySaving: null,
		};
	},
	computed: {
		sensors() {
			return this.$stores.sensorStore.sensorsByMeasurement;
		},
		actions() {
			return this.$stores.actionStore.actionsArr;
		},
		displayedEvents() {
			return this.events.concat(this.newEvents);
		},
	},
	methods: {
		addEvent() {
			this.newEvents.push({
				name: null,
				is_enabled: true,
				scheduled_time: null,
				conditions: [],
				actions: [],
				logic: 'AND',
			});
		},
		saveChanges(event, index) {
			this.currentlySaving = event._id;
			event?._id ? this.updateEvent(event) : this.createEvent(event, index);
		},
		createEvent(event, index) {
			this.$stores.eventStore.createEvent(event)
			.then(() => {
				this.events = this.$stores.eventStore.eventsArr.slice();
				this.newEvents.splice(index, 1);
				this.currentlySaving = null;
			});
		},
		updateEvent(event) {
			this.$stores.eventStore.updateEvent(event)
			.then(() => {
				this.events = this.$stores.eventStore.eventsArr.slice();
				this.currentlySaving = null;
			});
		},
		deleteEvent(event) {
			this.$stores.eventStore.deleteEvent(event)
			.then(() => {
				this.events = this.$stores.eventStore.eventsArr.slice();
			});
		},
		addCondition(event) {
			event.conditions.push({
				type: null,
				value: null,
			});
		},
		deleteCondition(event, index) {
			event.conditions.splice(index, 1);
		},
		addAction(event) {
			event.actions.push(null);
		},
		deleteAction(event, index) {
			event.actions.splice(index);
		},
	},
	mounted() {
		this.events = this.$stores.eventStore.eventsArr.slice();
	},
};
</script>
<style lang="scss">
.events {
	max-height: calc(100vh - 60px);

	overflow-y: auto;

	.el-card {

		overflow-y: auto;

		.el-card__body {
			padding: 0 !important;

			.el-collapse-item__header {
				.el-tag {
					margin-right: 7px;
				}
			}
		}
	}
}
</style>
