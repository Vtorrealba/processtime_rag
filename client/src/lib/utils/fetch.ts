import { PUBLIC_API_URL } from "$env/static/public";

const Fetch = () => {
	return async (url: string, options?: RequestInit) => {
		const defaultOptions: { Authorization?: string } = {};

		const state = JSON.parse(localStorage.getItem("user") || "{}");

		if (state?.state?.token) {
			defaultOptions.Authorization = `Bearer ${state.state.token}`;
		}

		const apiUrl = `${PUBLIC_API_URL}/${url}`;
		const requestOptions = {
			...options,
			headers: new Headers({
				"Content-Type": "application/json",
				...defaultOptions,
				...options?.headers,
			}),
		};
		const response = await fetch(apiUrl, requestOptions);

		return response;
	};
};

export default Fetch();
