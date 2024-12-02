<script lang="ts">
import gsap from "gsap";
import { onMount } from "svelte";
import P from "../typography/p.svelte";
import { Card } from "../ui/card";
import CardContent from "../ui/card/card-content.svelte";
import AssistantAvatar from "./assistant-avatar.svelte";
import UserAvatar from "./user-avatar.svelte";

import { ERole, type IMessage } from "$lib/schemas/message";
import Services from "$lib/services";
import { ThumbsDown, ThumbsUp } from "lucide-svelte";
import Button from "../ui/button/button.svelte";

let { message }: { message: IMessage } = $props();
let isAi = message.role === ERole.Assistant;

let isLiked: boolean | undefined = $state(undefined);

let uniqueId = `m${Math.random().toString(36).substring(2, 15)}`;

$effect(() => {
	if (isLiked !== undefined) {
		Services.chat.toggleMessageReaction(message.content, isLiked);
	}
});

onMount(() => {
	gsap.fromTo(
		`#${uniqueId}`,
		{
			opacity: 0,
			y: 5,
			duration: 0.2,
		},
		{
			opacity: 1,
			y: 0,
			duration: 0.2,
		},
	);
});
</script>

<div id={uniqueId} class="mb-4">
  <div class="flex gap-4 {isAi ? 'justify-start' : 'justify-end'}">
    {#if isAi}
      <AssistantAvatar isAssistant />
    {/if}

    <Card
      class="flex flex-col max-w-[70%] text-gray-800 {isAi
        ? 'bg-white '
        : 'bg-blue-50 text-blue-900'}"
    >
      <CardContent class="px-4 py-2">
        <P class="text-sm sm:text-base">{message.content}</P>
      </CardContent>
    </Card>

    {#if !isAi}
      <UserAvatar />
    {/if}
  </div>
  {#if isAi}
    <div class="flex justify-start items-center mt-1.5 ml-14 gap-2">
      <Button
        size="icon"
        title="Respuesta buena"
        variant={isLiked === undefined
          ? 'ghost'
          : isLiked
            ? undefined
            : 'ghost'}
        onclick={() => (isLiked = true)}
      >
        <ThumbsUp class="w-5 h-5" />
      </Button>
      <Button
        size="icon"
        title="Mala respuesta"
        variant={isLiked === undefined
          ? 'ghost'
          : isLiked
            ? 'ghost'
            : undefined}
        onclick={() => (isLiked = false)}
      >
        <ThumbsDown class="w-5 h-5" />
      </Button>
    </div>
  {/if}
</div>
