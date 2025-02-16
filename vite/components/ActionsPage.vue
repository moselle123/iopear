<template>
	<el-container direction="vertical" class="actions">
		<el-text class="title">Actions</el-text>
		<el-text>Create an action to control actuators such as a grow light. Add an action to an event to trigger your actions.</el-text>
		<el-row class="page-header">
			<el-alert v-if="newActions.length" type="warning" title="Please save changes before moving on." />
			<el-button type="primary" @click="addAction">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 144L48 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l144 0 0 144c0 17.7 14.3 32 32 32s32-14.3 32-32l0-144 144 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-144 0 0-144z"/></svg>
				Create Action
			</el-button>
		</el-row>
		<el-text v-if=" ! (actions.length || newActions.length)" class="no-content">No Actions to Display</el-text>
		<el-card v-else>
			<el-collapse accordion>
				<el-collapse-item v-for="(action, index) in displayedActions" :key="index" :title="action._id ? action.name : 'New Action'" :name="index">
					<el-form label-position="top">
						<el-row class="grid">
							<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
								<el-form-item label="Name">
									<el-input v-model="action.name" placeholder="Describe this action" />
								</el-form-item>
							</el-col>
							<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
								<el-form-item label="Actuator">
									<el-select v-model="action.actuator_id">
										<el-option v-for="actuator in actuators" :key="actuator" :label="actuator.name" :value="actuator._id" />
									</el-select>
								</el-form-item>
								<el-form-item label="Actuator State">
									<el-switch v-model="action.actuator_state" active-text="On" inactive-text="Off"/>
								</el-form-item>
							</el-col>
						</el-row>
					</el-form>
					<el-divider />
					<el-row justify="end">
						<el-button type="primary" v-if="action?._id" @click="triggerAction(action._id)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-242.7c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32L64 32zm0 96c0-17.7 14.3-32 32-32l192 0c17.7 0 32 14.3 32 32l0 64c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-64zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
							Trigger Action
						</el-button>
						<el-button type="primary" v-if="action?._id" @click="deleteAction(action)">
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M64 32C28.7 32 0 60.7 0 96L0 416c0 35.3 28.7 64 64 64l320 0c35.3 0 64-28.7 64-64l0-242.7c0-17-6.7-33.3-18.7-45.3L352 50.7C340 38.7 323.7 32 306.7 32L64 32zm0 96c0-17.7 14.3-32 32-32l192 0c17.7 0 32 14.3 32 32l0 64c0 17.7-14.3 32-32 32L96 224c-17.7 0-32-14.3-32-32l0-64zM224 288a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
							Delete Action
						</el-button>
						<el-button type="primary" @click="saveChanges(action)">
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
			newActions: [],
		};
	},
	computed: {
		actions() {
			return this.$stores.actionStore.actionsArr;
		},
		actuators() {
			return this.$stores.actuatorStore.actuatorsArr;
		},
		displayedActions() {
			return this.actions.concat(this.newActions);
		},
	},
	methods: {
		addAction() {
			this.newActions.push({
				name: null,
				actuator_id: null,
				actuator_state: true,
			});
		},
		saveChanges(action, index) {
			action?._id ? this.updateAction(action) : this.createAction(action, index);
		},
		createAction(action, index) {
			this.$stores.actionStore.createAction(action)
			.then(() => this.newActions.splice(index, 1));
		},
		updateAction(action) {
			this.$stores.eventStore.updateAction(action);
		},
		deleteAction(action) {
			this.$stores.actionStore.deleteAction(action);
		},
		triggerAction(action_id) {
			this.$stores.actionStore.triggerAction(action_id);
		},
	},
};
</script>

<style lang="scss">
.actions {
	max-height: calc(100vh - 60px);

	overflow-y: auto;

	.el-card {

		overflow-y: auto;

		.el-card__body {
			padding: 0 !important;
		}
	}
}
</style>
