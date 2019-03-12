<template>
  <div> 
    <highlight-code :lang="syntax" class="nt-hljs">
      {{ code }}
		</highlight-code>
  </div>
</template>

<script>
    export default {
        name: "TextPreview",
        props: ["file"],
        data () {
          return {
            code: "",
          }
        },
        computed: {
          syntax() { return this.file.file_text_info.syntax_highlighting;},
          url() { return this.file.file_content.startsWith('/') ? this.$backend_url + this.file.file_content : this.file.file_content;}
        },
        model: {
          prop: "file",
          event: "input"
        },
        async mounted () {
          await this.$api.GetFile(this.url)
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