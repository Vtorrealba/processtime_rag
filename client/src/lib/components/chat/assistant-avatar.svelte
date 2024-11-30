<script>
import { Bot, BotMessageSquare } from "lucide-svelte";

import { Avatar, AvatarFallback } from "../ui/avatar";

let { class: className = "", isAssistant = false } = $props();
</script>

<Avatar>
  <AvatarFallback>
    {#if isAssistant}
      <BotMessageSquare class="w-5 h-5 text-blue-900 {className}" />
    {:else}
      <Bot class="w-5 h-5 text-blue-900 {className}" />
    {/if}
  </AvatarFallback>
</Avatar>
