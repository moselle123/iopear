<template>
	<el-container class="line-chart" direction="vertical">
		<el-text v-if="loading" size="large" class="loading">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
			Loading data analysis
		</el-text>
		<canvas ref="chart"></canvas>
	</el-container>
</template>
<script>
export default {
	props: {
		sensor: {
			type: Object,
		},
		dateRange: {
			type: Array,
		},
		step: {
			type: String,
		},
		measurement: {
			type: String,
		},
	},
	data() {
		return {
			loading: true,
		};
	},
	computed: {
		color() {
			switch (this.measurement) {
				case 'temperature':
					return '#c72222';
				case 'humidity':
					return '#2a0b8f';
				case 'soil_moisture':
					return '#49afd1';
				case 'soil_temperature':
					return '#c72222';
				case 'lux':
					return '#fcc26a';
				default:
					return
			};
		},
	},
	methods: {
		loadChart() {
			let values = this.sensor.readings
			.filter((reading) => {
				return reading.measurement === this.measurement && reading.timestamp >= this.dateRange[0] && reading.timestamp < this.dateRange[1];
			})
			.map((reading) => ({ x: reading.timestamp, y: reading.value }));

			let steps = [];
			let stepCount = moment(this.dateRange[1]).diff(moment(this.dateRange[0]), this.step);
			for (let i = 0; i <= stepCount; i++) {
				steps.push(moment(this.dateRange[0]).clone().add(i, this.step).format('YYYY-MM-DD HH:mm'));
			}

			new Chart(this.$refs.chart.getContext('2d'), {
				type: 'line',
				data: {
					labels: steps,
					datasets: [{
						label: this.measurement,
						data: values,
						borderColor: this.color,
						borderWidth: 1
					}],
				},
				options: {
					responsive: true,
					scales: {y: {beginAtZero: true}},
					scales: {
						x: {
							type: 'time',
							time: {
								unit: this.step,
							},
						},
					},
				},
			});

			this.loading = false;
		},
	},
	mounted() {
		this.loadChart();
	}
};
</script>
<style lang="scss" scoped>
.line-chart {

}
</style>
