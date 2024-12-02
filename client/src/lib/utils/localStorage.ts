export function getLocalStorage<T>(key: string): T | null {
	if (typeof window === "undefined") {
		throw Error("Cannot use server side");
	}

	const existing = localStorage.getItem(key);

	return existing ? JSON.parse(existing) : null;
}
