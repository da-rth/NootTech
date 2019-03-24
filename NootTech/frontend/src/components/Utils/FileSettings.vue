<template>
  <div id="FileSettings" >

    <b-form v-if="file">
    <b-input-group prepend="Filename:">
      <b-form-input id=fileName :value="fileName" aria-describedby="basic-addon3"/>
      <div class="input-group-prepend">
        <span class="input-group-text" id="basic-addon3">{{file.file_ext}}</span>
      </div>
    </b-input-group>
   </b-form>

  </div>
</template>

<script>
  export default {
    name: "NtFileSettings",
    props: ["file"],
    computed: {
      fileName() {
        return this.file.original_filename.split(this.file.file_ext)[0]
      }
    },
    methods: {
      fileNameValidator(newName) {
        // TODO: avoid weird characters like tags
      }
    },
  }
</script>

<style scoped>
</style>