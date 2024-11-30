<script lang="ts">
const { children, class: className = "" } = $props();
</script>
<p class="text-muted-foreground text-xl {className}">{@render children()}</p>