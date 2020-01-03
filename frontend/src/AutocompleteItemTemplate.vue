<template>
  <div style="background-color: yellow">
    <span>{{ item }}</span>
  </div>
</template>

<script>
    export default {
        name: "AutocompleteItemTemplate",
        props: {
          item: { required: true },
          searchText: { required: true }
        }
    }
</script>

<style scoped>

</style>