import { usePlantStore } from '../stores/usePlantStore';

export default {
	install(app) {
		app.config.globalProperties.$stores = {
			plantStore: usePlantStore()
		};
	}
};
