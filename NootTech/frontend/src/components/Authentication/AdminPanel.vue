<template>
 <div v-if="$store.state.settings && $store.state.settings.is_superuser" class="container">
   <b-modal
    v-if="selectedReport"
    header-bg-variant="dark"
    body-bg-variant="dark"
    footer-bg-variant="dark"
    header-border-variant="dark"
    footer-border-variant="dark"
    ref="banModal"
    :title="`Ban the user ${selectedReport.reported_file.user.username}`"
    ok-title="Ban"
    ok-variant="danger"
    @ok="banUser"
    @hidden="resetBanPayload"
    >
    <b-form>
      <b-form-group
        label="Reason to ban the user"
        label-for="banReason"
        description="Please provide a reason for the ban">
        <b-form-textarea id="banReason" v-model="banPayload.reason" rows="3" max-rows="10"/>
      </b-form-group>

    </b-form>
   </b-modal>
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
            <b-button variant="danger" @click="banUserButton(report)">Ban user</b-button>
            <b-button variant="danger" @click="deleteFile(report)">Delete resource</b-button>
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
      selectedReport: null,
      config: config,
      banPayload: {
        user: 0,
        reason: "",
      }
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
      try {
        let response = await this.$api.WarnUser(
                      {reason: `${report.reason_title}\n${report.reason_body}`,
                       warned_user: `${report.reported_file.user.id}`})
      } catch(e) {
        console.log("USER WARNING FAILED: ", e.response);
      }
    },
    resetBanPayload() {
      this.banPayload = {
        user: 0,
        reason: "",
      }
    },
    banUserButton(report) {
      this.selectedReport = report;
      this.banPayload.user = report.reported_file.user.id;
      this.$nextTick(() => {
        this.$refs.banModal.show();
      })
    },
    async banUser() {
      try {
        await this.$api.BanUser(this.banPayload);
      } catch(e) {
        console.log("USER BAN FAILED: ", e.response);
      }
    },

    async deleteFile(report) {
      try {
        console.log("Deleting the file " + report.reported_file.id)
      } catch(e) {
        console.log("FILE DELETION FAILED: ", e.response)
      }
    }
    
 },
  async mounted() {
    try {
      let response = await this.$api.GetReports();
      this.resetBanPayload();
      this.reports = response.data;
    } catch(e) {
      console.log(e.response);
    }
  }
}

</script>

<style>
</style>