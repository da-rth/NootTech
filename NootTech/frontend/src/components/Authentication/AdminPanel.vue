<template>
  <div v-if="$store.state.settings && $store.state.settings.is_superuser">
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
      centered
      @hidden="resetBanPayload">
      <b-form>
        <b-form-group
          label="Reason to ban the user"
          label-for="banReason"
          description="Please provide a reason for the ban">
          <b-form-textarea id="banReason" v-model="banPayload.reason" rows="3" max-rows="10" required/>
        </b-form-group>
      </b-form>
    </b-modal>

    <b-modal
      v-if="selectedReport"
      header-bg-variant="dark"
      body-bg-variant="dark"
      footer-bg-variant="dark"
      header-border-variant="dark"
      footer-border-variant="dark"
      ref="warnModal"
      :title="`Warn the user ${selectedReport.reported_file.user.username}`"
      ok-title="Warn"
      ok-variant="danger"
      @ok="banUser"
      centered
      @hidden="resetBanPayload">
      <b-form>
        <b-form-group
          label="Reason for warning user:"
          label-for="warnReason"
          description="Please provide a reason for the warning">
          <b-form-textarea id="banReason" v-model="banPayload.reason" rows="3" max-rows="10" required />
        </b-form-group>
      </b-form>
    </b-modal>


  <b-modal
    v-if="selectedReport"
    header-bg-variant="dark"
    body-bg-variant="dark"
    centered
    footer-bg-variant="dark"
    header-border-variant="dark"
    footer-border-variant="dark"
    ref="userModal"
    :title="`Information on the user ${selectedReport.reported_file.user.username}`"
    
    >
    <p>Username: {{selectedReport.reported_file.user.username}}</p>
    <p>Email: {{selectedReport.reported_file.user.email}}</p>
    <p>Warnings: {{selectedReport.reported_file.user.warnings}}</p>
  </b-modal>

   <h1 class="report-heading">Reported Files</h1>
    <table class="table bg-dark striped">
      <thead>
        <tr>
          <td scope="col" align="center">Date</td>
          <td scope="col" align="center">Resource</td>
          <td scope="col" align="center">User</td>
          <td scope="col" align="center">Actions</td>
        </tr>
      </thead>
      <tbody>
        <tr v-for="report in reports" :key="report.id">
          <td scope="col" align="center">
            {{printableDate(report.date)}}
          </td>
          <td scope="col" align="center">
            <NtBadge :value="report.reported_file"
            :style="{width: `13rem`}"
            />
          </td>
          <td scope="col" align="center">
            <b-button class="reported-user-btn" @click="showUserModal(report)">{{report.reported_file.user.username}}</b-button>
          </td>
          <td scope="col" align="center">
            <b-button class="warn-btn" variant="warning" @click="warnUserButton(report)">Warn</b-button>
            <b-button class="ban-btn" variant="danger" @click="banUserButton(report)">Ban</b-button>
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
        warned_user: 0,
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
        warned_user: 0,
        reason: "",
      }
    },
    banUserButton(report) {
      this.selectedReport = report;
      this.banPayload.warned_user = report.reported_file.user.id;
      this.$nextTick(() => {
        this.$refs.banModal.show();
      })
    },

    warnUserButton(report) {
      this.selectedReport = report;
      this.banPayload.warned_user = report.reported_file.user.id;
      this.$nextTick(() => {
        this.$refs.warnModal.show();
      })
    },


    showUserModal(report) {
      this.selectedReport = report
      this.$nextTick(() => {
        this.$refs.userModal.show();
      })
    },
    async banUser() {
      try {
        await this.$api.BanUser(this.banPayload);
      } catch(e) {
        console.log("USER BAN FAILED: ", e.response);
      }
    },
 },
  async mounted() {
    try {
      let response = await this.$api.GetReports();
      this.resetBanPayload();
      this.reports = response.data;
    } catch(e) {
      console.log(e.response);
    }
  },

  beforeMount() {
    if (this.$store.state.settings && !this.$store.state.settings.is_superuser) {
      console.log("User not admin... redirecting!")
      this.$router.push("/");
    }
  },
}

</script>

<style>

table.bg-dark.striped {
  background-color: #1f1f1f !important;
  margin: 30px;
  border: 1px solid #000;
  width: 90%;
  margin: 0 auto;
}

.report-heading {
    text-align: center;
    padding: 20px;
}

table.bg-dark.striped td {
  border: 1px solid #000;
}

.reported-user-btn {
  background-color: transparent !important;
  border: 1px solid #3d3d3d !important;
  width: 100%;
}

.warn-btn, .ban-btn {
  width: 40%;
}
</style>