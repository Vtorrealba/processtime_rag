<script lang="ts">
import { messagePayloadSchema } from "$lib/schemas/message";
import { chatStore } from "$lib/store/chat.svelte.js";
import { Send } from "lucide-svelte";
import { z } from "zod";
import Button from "../ui/button/button.svelte";
import Input from "../ui/input/input.svelte";

let { sendMessage } = $props();

let message = $state("");
let errorMessage = $state("");

async function handleSubmit(e: SubmitEvent) {
	e.preventDefault();

	try {
		const newMessage = await messagePayloadSchema.parseAsync({
			question: message,
		});

		sendMessage(newMessage.question);
		message = "";
	} catch (error) {
		if (error instanceof z.ZodError) {
			errorMessage = error.errors[0].message;
		} else {
			errorMessage = "Ocurrió un error desconocido";
			console.error(error);
		}
	}
}
</script>

<form onsubmit={handleSubmit} class="flex gap-2 md:pb-10 pb-5 px-2 md:px-0">
  <div class="w-full relative">
    {#if errorMessage}
      <p class=" absolute text-red-500 text-sm bottom-[3rem]">
        {errorMessage}
      </p>
    {/if}

    <Input
      aria-errormessage={errorMessage}
      autofocus
      type="text"
      maxlength={150}
      bind:value={message}
      placeholder="Escribe un mensaje..."
      class="py-4 px-5 text-lg"
    />
  </div>

  <Button
    class="py-4 w-20"
    disabled={message.trim() === '' || chatStore.isTyping}
    type="submit"
    title="Enviar"
  >
    <Send class="w-5 h-5" />
  </Button>
</form>
