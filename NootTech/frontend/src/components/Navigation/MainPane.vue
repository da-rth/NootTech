<template>
  <div class="container text-light" id="mainPane">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "NmMainPane",
  props: ["title"],
  created() {
    document.title = this.title
  }
}
</script>