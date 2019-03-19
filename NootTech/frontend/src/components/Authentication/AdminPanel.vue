<template>
 <div v-if="$store.state.settings && $store.state.settings.is_superuser" class="container">
   <h2>List of reported files</h2>
    <table class="table bg-dark striped">
      <thead>
        <tr>
          <td scope="col">Date</td>
          <td scope="col">Resource name</td>
          <td scope="col">Actions</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="report in reports" :key="report.id">
          <td scope="col">
            {{report.date}}
          </td>
          <td scope="col">
            <a :href="`http://localhost:8000/media/${report.file_url}`">{{report.file_gen_name}}</a>
          </td>
          <td scope="col">
            To implement!
          </td>
        </tr>
      </tbody>
    </table>
 </div>
</template>

<script>
import config from '../../config.json';
export default {
  name: "AdminPanel",
  data() {
    return {
      reports: []
    }
  },
  async mounted() {
    try {
      let response = await this.$api.GetReports();
        this.reports = response.data;
    } catch(e) {
      console.log(e.response);
    }
  }
}

</script>

<style>
</style>