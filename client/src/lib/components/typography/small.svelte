<script lang="ts">
const { children, class: className = "" } = $props();
</script>

<small class="text-sm font-medium leading-none {className}">{@render children()}</small>