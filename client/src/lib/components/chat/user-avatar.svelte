<script>
import { User } from "lucide-svelte";

import { Avatar, AvatarFallback } from "../ui/avatar";

let { class: className = "" } = $props();
</script>
<Avatar>
  <AvatarFallback><User class="w-5 h-5 text-black {className}" /></AvatarFallback>
</Avatar>