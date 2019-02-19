<template>
    <b-card
        title="Cart title"
        img-alg="Image"
        img-top
        tag="article"
        style="max-width: 20rem;"
        class="mb-2"
        v-bind:value="value"
        v-on:input="$emit('input', $event.target.value)"
        :img-src="value.thumbnail"
    >
    </b-card>
</template>

<script>
  export default {
    name: "NtImageBadge",
    props: ["value"],
    created: function() {
        console.log("Hello there!")
        console.log(this.value)
    }
  }
</script>