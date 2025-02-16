import './main.scss';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import storesPlugin from './plugins/storesPlugin';
import {io} from 'socket.io-client';

import axios from 'axios';
window.axios = axios;


import { Chart as ChartJS, Title, Tooltip, Legend, LineController, LineElement, PointElement, LinearScale, TimeScale, CategoryScale, Filler } from 'chart.js';
import 'chartjs-adapter-moment';
ChartJS.register(Title, Tooltip, Legend, LineController, LineElement, PointElement, LinearScale, TimeScale, CategoryScale, Filler);
window.Chart = ChartJS;

import moment from 'moment';
window.moment = moment;

if (location.port !== '5173') {
	window.host = 'http://' + location.hostname + ':5000';
	window.socket = io('http://' + location.hostname + ':5000');
} else {
	window.host = 'http://100.65.155.12:5000'
	window.socket = io('http://100.65.155.12:5000');
}

window.socket.on("connect", () => console.debug('websocket connected'));

import ElementPlus from 'element-plus';
import 'element-plus/theme-chalk/src/dark/var.scss';
import './theme.scss';
import App from './App.vue';

import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from './components/WelcomePage.vue';
import DashboardPage from './components/DashboardPage.vue';
import DataPage from './components/DataPage.vue';
import SensorsPage from './components/SensorsPage.vue';
import EventsPage from './components/EventsPage.vue';
import ActionsPage from './components/ActionsPage.vue';

import LineChart from './components/LineChart.vue';
import NotificationsPopup from './components/NotificationsPopup.vue';

const routes = [
	{
		path: '/',
		name: 'Dashboard',
		component: DashboardPage,
		props: true,
	},
	{
		path: '/events',
		name: 'events',
		component: EventsPage,
		props: true,
	},
	{
		path: '/actions',
		name: 'actions',
		component: ActionsPage,
		props: true,
	},
	{
		path: '/sensors',
		name: 'sensors',
		component: SensorsPage,
		props: true,
	},
	{
		path: '/data',
		name: 'Data',
		component: DataPage,
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
app.component('NotificationsPopup', NotificationsPopup);
app.use(createPinia());
app.use(storesPlugin);
app.use(router);
app.use(ElementPlus);
app.mount('#app');