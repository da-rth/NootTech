<template>
  <div>

    <h1 v-if="$store.state.user.authenticated">You are logged in! Files will appear here!</h1>

    <nt-main-pane title="NootTech: More than meets the m-eye-nd" v-else>
        <b-jumbotron header="Discover NooTech!"
                class="bg-dark"
                lead="This is a simple hero unit">
          <b-button variant="primary" href="#">More Info</b-button>
        </b-jumbotron>
      </nt-main-pane>
    </div>
  
</template>

<script>
import NtMainPane from './Navigation/MainPane.vue';

export default {
    name: "Base",
    components: {NtMainPane}
}
</script>

<style scoped>

</style>
