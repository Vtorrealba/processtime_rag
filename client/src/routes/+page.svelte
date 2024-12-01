<script lang="ts">
import AssistantAvatar from "$lib/components/chat/assistant-avatar.svelte";
import ChatInput from "$lib/components/chat/input.svelte";
import ChatMessage from "$lib/components/chat/message.svelte";
import Suggestion from "$lib/components/chat/suggestion.svelte";
import TypingIndicator from "$lib/components/chat/typing-indicator.svelte";
import { ERole, messageSchema } from "$lib/schemas/message";
import Services from "$lib/services";
import { chatStore } from "$lib/store/chat.svelte.js";

/** @type {HTMLElement} */
let chatContainer: HTMLElement;

async function handleSendMessage(content: string) {
	const newMessage = {
		content,
		role: ERole.User,
		timestamp: new Date().toLocaleDateString(),
	};

	chatStore.isTyping = true;
	chatStore.messages = [...chatStore.messages, messageSchema.parse(newMessage)];

	const makeCompletion = await Services.chat.makeCompletion({
		question: newMessage.content,
	});

	chatStore.isTyping = false;
	chatStore.messages = [...chatStore.messages, makeCompletion];
}

function scrollToBottom() {
	setTimeout(() => {
		chatContainer.scrollTop = chatContainer.scrollHeight;
	}, 0);
}

$effect(() => {
	if (chatContainer && chatStore.messages) {
		scrollToBottom();
	}
});
</script>

<svelte:head>
  <title>Chat con IA</title>
  <meta
    name="description"
    content="Aplicación de chat con inteligencia artificial"
  />
</svelte:head>

<div class="flex flex-col h-dvh bg-white">
  <!-- Header -->
  <header
    class="bg-white border-b pt-0 sm:py-4 flex justify-center px-4 sm:px-0"
  >
    <div class="flex items-center gap-3 max-w-3xl">
      <AssistantAvatar />
      <div>
        <h1 class="md:text-xl font-semibold text-blue-900">
          Asistente Virtual
        </h1>
        <p class="text-muted-foreground text-xs md:text-sm">
          <span class="hidden md:inline">
            Estoy acá para ayudarte y resolver de manera rápida tus dudas.
          </span>
          Puedes consultar información de la empresa como Políticas, Procedimientos,
          Productos y sus características
        </p>
      </div>
    </div>
  </header>

  <!-- Chat Messages -->
  <main
    bind:this={chatContainer}
    class="flex-1 overflow-y-auto py-6 px-4 sm:px-0"
  >
    <div class="max-w-3xl mx-auto space-y-4">
      {#each chatStore.messages as message}
        <ChatMessage {message} />
      {/each}
      {#if chatStore.isTyping}
        <TypingIndicator />
      {/if}
    </div>
  </main>
  <!-- suggestions -->
  <Suggestion />

  <!-- Input Area -->
  <div>
    <div class="max-w-3xl mx-auto">
      <ChatInput sendMessage={handleSendMessage} />
    </div>
  </div>
</div>
