import { usePlantStore } from '../stores/usePlantStore';
import { useSensorStore } from '../stores/useSensorStore';
import { useEventStore } from '../stores/useEventStore';

export default {
	install(app) {
		app.config.globalProperties.$stores = {
			plantStore: usePlantStore(),
			sensorStore: useSensorStore(),
			eventStore: useEventStore(),
		};
	}
};
