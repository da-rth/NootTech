<template>
    <highlight-code :lang="syntax" class="nt-hljs">
      {{ code }}
		</highlight-code>
</template>

<script>
    export default {
        name: "TextPreview",
        props: ["file"],
        data () {
          return {
            code: "",
            syntax: ""
          }
        },
        async mounted () {
          this.syntax = this.file.file_text_info.syntax_highlighting;

          let url = this.file.file_content.startsWith('/') ? this.$backend_url+this.file.file_content : this.file.file_content;

          await this.$api.GetFile(url)
          .then(response => {
            this.code = response.data;
          })
          .catch(e => {
            this.code = 'Whoops! Could not get file contents :(';
          });
        },
        beforeDestroy() {
            console.log('fileblock destroyed')
        }
    }
</script>

<style>
.hljs {
    background-color: rgba(0,0,0,0.2) !important;
    margin: 0px 50px;
    padding: 20px !important;
    overflow-y: scroll !important;
}
</style>

