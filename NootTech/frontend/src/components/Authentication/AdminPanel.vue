<template>
 <div v-if="$store.state.settings && $store.state.settings.is_superuser" class="container">
   <h2>List of reported files</h2>
    <table class="table bg-dark striped">
      <thead>
        <tr>
          <td scope="col">Date</td>
          <td scope="col">Resource</td>
          <td scope="col">User</td>
          <td scope="col">Actions</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="report in reports" :key="report.id">
          <td scope="col">
            {{printableDate(report.date)}}
          </td>
          <td scope="col">
            <NtBadge :value="report.reported_file"
            :style="{width: `13rem`}"
            />
          </td>
          <td scope="col">
            <a :href="'mailto:'+report.reported_file.user.email">{{report.reported_file.user.username}}</a>
          </td>
          <td scope="col">
            <b-button variant="warning" @click="warnUser(report)">Warn user</b-button>
            <b-button variant="danger">Ban user</b-button>
            <b-button variant="danger">Delete resource</b-button>
          </td>
        </tr>
      </tbody>
    </table>
 </div>
</template>

<script>
import config from '../../config.json';
import NtBadge from '../Utils/Badge.vue';
export default {
  name: "AdminPanel",
  data() {
    return {
      reports: [],
      config: config,
    }
  },
  components: {NtBadge},
  methods: {
    printableDate(serverDate) {
      let datetime = serverDate.split('T')
      datetime[1] = datetime[1].split('.')[0] // discard microseconds

      return `${datetime[0]} at ${datetime[1]}`;
    },
    /**
     * Warn an user
     * @param {Object} report
     */
    async warnUser(report) {
      console.log("Warning the user " + report.reported_file.user.username)
      let response = await this.$api.WarnUser(
                      {reason: `${report.reason_title}\n${report.reason_body}`,
                       warned_user: `${report.reported_file.user.id}`})
    }
 },
  async mounted() {
    try {
      let response = await this.$api.GetReports();
      this.reports = response.data;
      console.log(this.reports);
    } catch(e) {
      console.log(e.response);
    }
  }
}

</script>

<style>
</style>