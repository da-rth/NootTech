<template>
  <div>
    <H3>
      This information is being displayed by VueJS but taken from
      <a v-bind:href="this.$api_url+'/list-users/'">this API url</a>
    </H3>

    <ul v-if="users && users.length">
      <li v-for="user of users">
        <p><strong>{{user.username}}</strong><br/>
        Joined: {{ user.date_joined }}<br/>
        Colour: <span v-bind:style="{ color: user.colour }">{{ user.colour }}</span><br/>
        Admin: {{ user.is_admin }}</p>
      </li>
    </ul>

    <ul v-if="errors && errors.length">
      <li v-for="error of errors">
        {{error.message}}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'app',
  data() {
    return {
      users: [],
      errors: []
    }
  },

  created() {
    console.log(this.$api_url+"/list-users");
    axios.get(this.$api_url+"/list-users")
    .then(response => {
      console.log(response);
      this.users = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  }
}
</script>
