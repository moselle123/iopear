<template>
	<el-card class="line-chart">
		<template #header><el-text>{{ title }} {{ formattedDate }}</el-text></template>
		<el-text v-if="loading" size="large" class="loading">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="spinner"><path d="M304 48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zm0 416a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM48 304a48 48 0 1 0 0-96 48 48 0 1 0 0 96zm464-48a48 48 0 1 0 -96 0 48 48 0 1 0 96 0zM142.9 437A48 48 0 1 0 75 369.1 48 48 0 1 0 142.9 437zm0-294.2A48 48 0 1 0 75 75a48 48 0 1 0 67.9 67.9zM369.1 437A48 48 0 1 0 437 369.1 48 48 0 1 0 369.1 437z"/></svg>
			Loading {{ title }} data
		</el-text>
		<canvas ref="chart"></canvas>
	</el-card>
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
		thresholdMin: {
			type: Number,
		},
		thresholdMax: {
			type: Number,
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
		formattedDate() {
			return '( ' + moment(this.dateRange[0]).format('DD/MM/YY HH:mm') + ' - ' + moment(this.dateRange[1]).format('DD/MM/YY HH:mm') + ')'
		},
		unit() {
			switch (this.measurement) {
				case 'temperature':
					return '°C';
				case 'humidity':
					return '%';
				case 'soil_moisture':
					return '%';
				case 'soil_temperature':
					return '°C';
				case 'light_intensity':
					return 'lx';
				case 'barometric_pressure':
					return 'hPa';
				case 'co2':
					return 'ppm';
				default:
					return '';
			};
		},
		color() {
			switch (this.measurement) {
				case 'temperature':
					return '#ff0000';
				case 'humidity':
					return '#e669ff';
				case 'soil_moisture':
					return '#2053f9';
				case 'soil_temperature':
					return '#90441b';
				case 'light_intensity':
					return '#ff8c2e';
				case 'barometric_pressure':
					return '#8dfa6c';
				case 'co2':
					return '#355054';
				default:
					return  '#000';
			};
		},
	},
	methods: {
		loadChart() {
			let values = this.readings
			.filter((reading) => {
				return reading.measurement === this.measurement && reading.timestamp >= this.dateRange[0] && reading.timestamp < this.dateRange[1];
			})
			.map((reading) => ({x: moment.utc(reading.timestamp).tz('Europe/London').toDate(), y: reading.value }));

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
					datasets: [
						{
							label: this.title,
							data: values,
							borderColor: this.color,
							borderWidth: 1
						},
						{
							label: "Threshold Min",
							data: steps.map((step) => ({ x: step, y: this.thresholdMin })),
							borderWidth: 1,
							pointRadius: 0,
							fill: false,
						},
						{
							label: "Threshold Max",
							data: steps.map((step) => ({ x: step, y: this.thresholdMax })),
							borderWidth: 1,
							fill: "-1",
							pointRadius: 0,
							backgroundColor: "rgba(0, 255, 0, 0.1)",
						},
					],
				},
				options: {
					responsive: true,
					plugins: {
						legend: { display: false},
						filler: { propagate: false } ,
					},
					scales: {
						y: {
							beginAtZero: false,
							suggestedMin: Math.min(...values.map(v => v.y)) - 5,
							suggestedMax: Math.max(...values.map(v => v.y)) + 5,
							title: { display: true, text: this.title + ' ( ' + this.unit + ' )'},
						},
						x: {
							type: 'time',
							time: {
								unit: this.step,
								displayFormats: {
									hour: 'HH:mm',
									minute: 'HH:mm',
									second: 'HH:mm:ss',
								},
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
