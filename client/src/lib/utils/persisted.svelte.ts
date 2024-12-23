export function persisted<T>(key: string, initial?: T) {
	if (typeof window === "undefined") {
		throw Error("Cannot use server side");
	}

	const existing = localStorage.getItem(key);

	let state = $state(existing ? JSON.parse(existing) : initial);

	$effect(() => {
		localStorage.setItem(key, JSON.stringify(state));
	});

	return {
		get value() {
			return state as T;
		},

		set value(new_state) {
			state = new_state as T;
		},

		reset() {
			state = initial as T;
		},
	};
}
