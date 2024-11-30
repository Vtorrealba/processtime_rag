import {
	ERole,
	type IMessage,
	type IMessagePayload,
	messageSchema,
} from "$lib/schemas/message";
import fetch from "$lib/utils/fetch";

export class Chat {
	static async makeCompletion(message: IMessagePayload): Promise<IMessage> {
		const aiResponse = messageSchema.parse({
			content:
				"Gracias por tu mensaje. Estoy procesando tu consulta y te responderé en breve.",
			role: ERole.Assistant,
			timestamp: new Date().toLocaleDateString(),
		});
		await new Promise((resolve) => setTimeout(resolve, 2000));
		return aiResponse;
	}

	static async getSuggestions(): Promise<string[]> {
		const suggestions = [
			"¿Como acepto una llamada?",
			"¿Cómo hacer un cobro?",
			"¿Cómo actualizo a un cliente?",
		];
		return suggestions;
	}

	static async toggleMessageReaction(messageID: string, isLiked: boolean) {
		const request = await fetch(`/message/${messageID}`, {
			method: "POST",
			body: JSON.stringify({ isLiked }),
			headers: {
				"Content-Type": "application/json",
			},
		});
		const response = await request.json();
		return isLiked;
	}
}
