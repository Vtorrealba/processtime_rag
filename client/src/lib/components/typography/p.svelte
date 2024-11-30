<script lang="ts">
const { children, class: className = "" } = $props();
</script>
<p class="[&:not(:first-child)]:mt-6 {className}">{@render children()}</p>