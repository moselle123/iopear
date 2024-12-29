import './main.scss';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import storesPlugin from './plugins/storesPlugin';

import axios from 'axios';
window.axios = axios;

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
import SettingsPage from './components/SettingsPage.vue';

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
app.component('WelcomePage', WelcomePage);
app.use(createPinia());
app.use(storesPlugin);
app.use(router);
app.use(ElementPlus);
app.mount('#app');