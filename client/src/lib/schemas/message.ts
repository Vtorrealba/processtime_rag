import { z } from "zod";

export enum ERole {
	User = "user",
	Assistant = "assistant",
}

export const roleSchema = z.enum([ERole.User, ERole.Assistant]);

export const messagePayloadSchema = z.object({
	question: z.string(),
});

export const messageSchema = z.object({
	role: roleSchema,
	content: z.string(),
	timestamp: z.string(),
});

export interface IMessagePayload extends z.infer<typeof messagePayloadSchema> {}

export interface IMessage extends z.infer<typeof messageSchema> {}
