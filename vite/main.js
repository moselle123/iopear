import './main.scss';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import storesPlugin from './plugins/storesPlugin';

import axios from 'axios';
window.axios = axios;


import { Chart as ChartJS, Title, Tooltip, Legend, LineController, LineElement, PointElement, LinearScale, TimeScale, CategoryScale } from 'chart.js';
import 'chartjs-adapter-moment';
ChartJS.register(Title, Tooltip, Legend, LineController, LineElement, PointElement, LinearScale, TimeScale, CategoryScale);
window.Chart = ChartJS;

import moment from 'moment';
window.moment = moment;

if (location.port !== '5173') {
	window.host = '/';
} else {
	window.host = 'http://100.65.155.12:5000'
}

import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/src/dark/var.scss';
import './theme.scss';
import App from './App.vue';

import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from './components/WelcomePage.vue';
import DashboardPage from './components/DashboardPage.vue';
import ConfigurePage from './components/ConfigurePage.vue';
import DataPage from './components/DataPage.vue';
import LogPage from './components/LogPage.vue';
import SettingsPage from './components/SettingsPage.vue';

import LineChart from './components/toolkit/LineChart.vue';
import SensorsConfiguration from './components/toolkit/SensorsConfiguration.vue';
import EventsConfiguration from './components/toolkit/EventsConfiguration.vue';
import ActionsConfiguration from './components/toolkit/ActionsConfiguration.vue';

const routes = [
	{
		path: '/',
		name: 'Dashboard',
		component: DashboardPage,
		props: true,
	},
	{
		path: '/configure',
		name: 'configure',
		component: ConfigurePage,
		props: true,
	},
	{
		path: '/data',
		name: 'Data',
		component: DataPage,
		props: true,
	},
	{
		path: '/log',
		name: 'Log',
		component: LogPage,
		props: true,
	},
	{
		path: '/settings',
		name: 'Settings',
		component: SettingsPage,
		props: true,
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes: routes,
});

const app = createApp(App);
const pinia = createPinia();
app.component('WelcomePage', WelcomePage);
app.component('LineChart', LineChart);
app.component('SensorsConfiguration', SensorsConfiguration);
app.component('EventsConfiguration', EventsConfiguration);
app.component('ActionsConfiguration', ActionsConfiguration);
app.use(createPinia());
app.use(storesPlugin);
app.use(router);
app.use(ElementPlus);
app.mount('#app');