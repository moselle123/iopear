<template>
	<el-container class="settings" direction="vertical" >
		<el-text class="title">Settings</el-text>
		<el-row justify="space-between">
			<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
				<el-card>
					<template #header>
						<el-text>Network</el-text>
						<el-text size="small">Update network settings or switch to Ethernet connection.</el-text>
					</template>
					<el-form label-width="150px" label-position="right" >
						<el-form-item label="WiFi">
							<el-switch v-model="config.network.wifi" />
						</el-form-item>
						<el-form-item label="WiFi SSID">
							<el-input v-model="config.network.ssid" />
						</el-form-item>
						<el-form-item label="WiFi Password">
							<el-input type="password" v-model="config.network.password" />
						</el-form-item>
					</el-form>
				</el-card>
				<el-card>
					<template #header>
						<el-text>Sensors</el-text>
						<el-text size="small">Select the sensors you want to activate for monitoring your plant's environment.</el-text>
					</template>
					<el-form label-width="250px" label-position="left" >
						<el-row justify="space-between">

							<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
								<el-form-item label="Soil Moisture & Soil Temperature">
									<el-switch v-model="config.network.wifi" />
								</el-form-item>
								<el-text size="small">Adafruit Soil Moisture Sensor</el-text>
								<el-form-item label="Air Temperature & Humidity">
									<el-switch v-model="config.network.wifi" />
								</el-form-item>
								<el-text size="small">SHT31</el-text>
								<el-form-item label="Light Intensity">
									<el-switch v-model="config.network.wifi" />
								</el-form-item>
								<el-text size="small">TSL2561</el-text>
							</el-col>
							<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
								<el-form-item label="Barometric Pressure">
									<el-switch v-model="config.network.wifi" />
								</el-form-item>
								<el-text size="small">BME280</el-text>
								<el-form-item label="CO2">
									<el-switch v-model="config.network.wifi" />
								</el-form-item>
								<el-text size="small">SCD40</el-text>
								<el-form-item label="Grow Lights & Watering">
									<el-switch v-model="config.network.wifi" />
								</el-form-item>
								<el-text size="small">Relay Module</el-text>

							</el-col>
						</el-row>
					</el-form>
				</el-card>
			</el-col>
			<el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
				<el-card>
					<template #header>
						<el-text>Preferences</el-text>
						<el-text size="small">Receive alerts and updates about your plant's status.</el-text>
					</template>
					<el-form label-position="right" >
						<el-form-item label="System Notifications">
							<el-switch v-model="config.preferences.notifications" />
						</el-form-item>
						<el-text>Receive alerts and updates about your plant's status.</el-text>
						<el-form-item label="Predictive Plant Health">
							<el-switch v-model="config.network.wifi" />
						</el-form-item>
						<el-text>Enable insights about potential plant health trends based on sensor data.</el-text>
					</el-form>
				</el-card>
			</el-col>
		</el-row>
	</el-container>
</template>
<script>
export default {
	data() {
		return {
		};
	},
};
</script>
<style lang="scss" scoped>
.settings {
	.el-col {
		padding: 0 0.5em;

		.el-card {
			margin-bottom: 1em;
		}
	}
}
</style>
