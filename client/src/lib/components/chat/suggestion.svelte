<script lang="ts">
import { ERole, messageSchema } from "$lib/schemas/message";
import Services from "$lib/services";
import { chatStore } from "$lib/store/chat.svelte";
import Placeholder from "@whizzes/svelte-placeholder";
import { onMount } from "svelte";
import { Button } from "../ui/button";

async function handleSendMessage(content: string) {
	const newMessage = {
		content,
		role: ERole.User,
		timestamp: new Date().toLocaleDateString(),
	};

	chatStore.isTyping = true;
	chatStore.messages = [...chatStore.messages, messageSchema.parse(newMessage)];

	const makeCompletion = await Services.chat.makeCompletion(newMessage);

	chatStore.isTyping = false;
	chatStore.messages = [...chatStore.messages, makeCompletion];
}

onMount(async () => {
	chatStore.isLoadingSuggestions = true;
	chatStore.suggestions = await Services.chat.getSuggestions();
	chatStore.isLoadingSuggestions = false;
});
</script>

{#if chatStore.messages.length < 2}
  <div class="max-w-3xl mx-auto mb-8 w-full px-2 md:px-0">
    <div class="flex justify-between flex-wrap gap-2">
      {#each chatStore.suggestions as suggestion}
        <Button variant="outline" onclick={() => handleSendMessage(suggestion)}>
          {suggestion}
        </Button>
      {:else}
        {#if chatStore.isLoadingSuggestions}
          <Button variant="outline">
            <Placeholder>
              <rect y="95" rx="3" ry="3" width="100%" height="10" />
            </Placeholder>
          </Button>
          <Button variant="outline">
            <Placeholder>
              <rect y="95" rx="3" ry="3" width="100%" height="10" />
            </Placeholder>
          </Button>
          <Button variant="outline">
            <Placeholder>
              <rect y="95" rx="3" ry="3" width="100%" height="10" />
            </Placeholder>
          </Button>
        {/if}
      {/each}
    </div>
  </div>
{/if}
