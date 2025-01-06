<template>
	<el-container class="line-chart" direction="vertical">
		<el-text v-if="loading" size="large" class="loading">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
			Loading {{ title }} data
		</el-text>
		<canvas ref="chart"></canvas>
	</el-container>
</template>
<script>
export default {
	props: {
		sensorName: {
			type: String,
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
			chart: null,
			loading: true,
			readings: [],
		};
	},
	watch: {
		dateRange: {
			immediate: true,
			handler() {
				this.loading = true;
				this.$stores.sensorStore.getReadingsByDateRange(this.sensorName, this.dateRange[0], this.dateRange[1], this.measurement)
				.then((data) => {
					this.readings = data;
					this.loadChart();
				});
			},
		},
	},
	computed: {
		title() {
			let title = this.measurement.replace('_', ' ').split(' ');
			title = title.map(word => word[0].toUpperCase() + word.substring(1));
			return title.join(' ');
		},
		unit() {
			switch (this.measurement) {
				case 'temperature':
					return '°C';
				case 'humidity':
					return '%';
				case 'soil moisture':
					return '%';
				case 'soil temperature':
					return '°C';
				case 'light intensity':
					return 'lx';
				default:
					return '';
			};
		},
		color() {
			switch (this.measurement) {
				case 'temperature':
					return '#c72222';
				case 'humidity':
					return '#2a0b8f';
				case 'soil moisture':
					return '#49afd1';
				case 'soil temperature':
					return '#c72222';
				case 'light intensity':
					return '#fcc26a';
				default:
					return '#000';
			};
		},
	},
	methods: {
		loadChart() {
			let values = this.readings
			.filter((reading) => {
				return reading.measurement === this.measurement && reading.timestamp >= this.dateRange[0] && reading.timestamp < this.dateRange[1];
			})
			.map((reading) => ({ x: reading.timestamp, y: reading.value }));

			let steps = [];
			let stepCount = moment(this.dateRange[1]).diff(moment(this.dateRange[0]), this.step);
			for (let i = 0; i <= stepCount; i++) {
				steps.push(moment(this.dateRange[0]).clone().add(i, this.step).format('YYYY-MM-DD HH:mm'));
			}
			if (this.chart) {
				this.chart.destroy();
				this.chart = null;
			}

			this.chart = new Chart(this.$refs.chart.getContext('2d'), {
				type: 'line',
				data: {
					labels: steps,
					datasets: [{
						label: this.title,
						data: values,
						borderColor: this.color,
						borderWidth: 1
					}],
				},
				options: {
					responsive: true,
					plugins: {
						title: {
							display: true,
							text: this.title + ' ( ' + moment(this.dateRange[0]).format('DD/MM/YY HH:mm') + ' - ' + moment(this.dateRange[1]).format('DD/MM/YY HH:mm') + ' )',
							padding: { top: 10, bottom: 20 },
						},
						legend: { display: false },
					},
					scales: {
						y: {
							beginAtZero: true,
							title: { display: true, text: this.title + ' ( ' + this.unit + ' )'},
						},
						x: {
							type: 'time',
							time: {
								unit: this.step,
							},
							title: { display: true, text: 'Time ( ' + this.step + 's )'}
						},
					},
				},
			});

			this.loading = false;
		},
	},
};
</script>
<style lang="scss" scoped>
.line-chart {
	.loading {
		margin-top: 3em;

		align-self: center !important;
	}
}
</style>
