import {
	ERole,
	type IMessage,
	type IMessagePayload,
	messageSchema,
} from "$lib/schemas/message";
import fetch from "$lib/utils/fetch";

export class Chat {
	static async makeCompletion(
		message: IMessagePayload,
		user_id: string | number,
	): Promise<IMessage> {
		const request = await fetch("/ask", {
			method: "POST",
			body: JSON.stringify({ question: message.question, id: Number(user_id) }),
			headers: {
				"Content-Type": "application/json",
			},
		});

		const response = await request.json();

		const aiResponse = messageSchema.parse({
			content: response.content,
			role: ERole.Assistant,
			timestamp: new Date().toLocaleDateString(),
		});
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
		/* 	const request = await fetch(`/message/${messageID}`, {
			method: "POST",
			body: JSON.stringify({ isLiked }),
			headers: {
				"Content-Type": "application/json",
			},
		});
		const response = await request.json(); */
		return isLiked;
	}
}
