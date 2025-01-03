import { usePlantStore } from '../stores/usePlantStore';
import { useSensorStore } from '../stores/useSensorStore';

export default {
	install(app) {
		app.config.globalProperties.$stores = {
			plantStore: usePlantStore(),
			sensorStore: useSensorStore(),
		};
	}
};
