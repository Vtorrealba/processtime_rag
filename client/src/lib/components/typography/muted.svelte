<script lang="ts">
const { children, class: className = "" } = $props();
</script>

<span class="text-muted-foreground text-sm {className}">{@render children()}</span>