<script lang="ts">
import { chatStore } from "$lib/store/chat.svelte.js";
import { Send } from "lucide-svelte";
import Button from "../ui/button/button.svelte";
import Input from "../ui/input/input.svelte";

let { sendMessage } = $props();

let message = $state("");

function handleSubmit(e: SubmitEvent) {
	e.preventDefault();
	if (message.trim()) {
		sendMessage(message);
		message = "";
	}
}
</script>

<form onsubmit={handleSubmit} class="flex gap-2 md:pb-10 pb-5 px-2 md:px-0">
  <Input
    autofocus
    type="text"
    bind:value={message}
    placeholder="Escribe un mensaje..."
    class="py-4 px-5 text-lg"
  />
  <Button
    class="py-4 w-20"
    disabled={message.trim() === '' || chatStore.isTyping}
    type="submit"
    title="Enviar"
  >
    <Send class="w-5 h-5" />
  </Button>
</form>
