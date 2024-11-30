import { ERole, type IMessage } from "$lib/schemas/message";

interface IChatStore {
	messages: IMessage[];
	isTyping: boolean;
	suggestions: string[];
	isLoadingSuggestions: boolean;
}

export const chatStore = $state<IChatStore>({
	messages: [
		{
			content: "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy?",
			role: ERole.Assistant,
			timestamp: new Date().toLocaleDateString(),
		},
	],
	isTyping: false,
	suggestions: [],
	isLoadingSuggestions: true,
});
