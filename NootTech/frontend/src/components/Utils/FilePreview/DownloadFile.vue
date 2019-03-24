<template>
  <div id="download-container">
    <b-button class="download-btn" v-bind:style="{borderColorHover: this.$root.colour}" v-on:click="downloadFile()">
      <font-awesome-icon icon="download"/> &nbsp;Download File ({{ file.file_size_str }})
      </b-button>

    <template v-if="file.virus_info" >
      <b-button class="virus-btn" :href="file.virus_info.permalink">
        <font-awesome-icon icon="shield-alt"/> &nbsp;Virus Total Info
        </b-button>
      <br/><br/>
      <span class="md5"><span v-bind:style="{color: this.$root.colour}">MD5:</span> {{ file.virus_info.md5 }}</span>
    </template>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: "DownloadFile",
    props: ['file'],
    computed: {
      // TODO: Possible LFI attacks?
      downloadURL : function () {
        return this.file.file_content.startsWith('/') ? this.$backend_url+this.file.file_content : this.file.file_content;
      }
    },
    methods: {
        downloadFile: function () {
          // from https://gist.github.com/javilobo8/097c30a233786be52070986d8cdb1743
          axios({
            url: this.downloadURL,
            method: 'GET',
            responseType: 'blob', // important
          }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', this.file.original_filename);
            document.body.appendChild(link);
            link.click();
          });
        }
    }
  }
</script>

<style scoped>
  #download-container {
    margin: 0 auto;
    width: 100%;
    margin: 40px 0;
    text-align: center;
  }

.download-btn, .virus-btn {
    color: white;
    margin: 10px 0;
    mix-blend-mode: difference;
    padding: 10px 20px;
    border: 1px solid rgba(255, 255, 255, 0.7);
    background-color: #202020;
    opacity: 0.88;
}
.download-btn:hover {
  opacity: 1;
  border: 1px solid #FFFFFF;
}

.virus-btn:hover {
  opacity: 1;
  background-color: #389dd3;
}

.md5 {
    background-color: rgba(0,0,0,0.5);
    padding: 6px 10px;
    border-radius: 5px;
    color: #a4a4a4;
}
</style>
