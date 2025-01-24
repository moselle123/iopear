import { usePlantStore } from '../stores/usePlantStore';
import { useSensorStore } from '../stores/useSensorStore';
import { useEventStore } from '../stores/useEventStore';
import { useActionStore } from '../stores/useActionStore';
import { useActuatorStore } from '../stores/useActuatorStore';

export default {
	install(app) {
		app.config.globalProperties.$stores = {
			plantStore: usePlantStore(),
			sensorStore: useSensorStore(),
			eventStore: useEventStore(),
			actionStore: useActionStore(),
			actuatorStore: useActuatorStore(),
		};
	}
};
