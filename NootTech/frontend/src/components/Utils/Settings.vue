<template>
  <div id="FileSettings" :ref="fileSettings">
    <h3>File settings</h3>
    <!-- by now let's just support renaming -->
    <b-form v-if="file">

    <label for="fileName">File name</label>
    <div class="input-group mb-3">
      <b-form-input id=fileName :value="fileName" aria-describedby="basic-addon3"/>
      <div class="input-group-prepend">
        <span class="input-group-text" id="basic-addon3">{{file.file_ext}}</span>
      </div>
    </div>
   </b-form>

  </div>
</template>

<script>
  export default {
    name: "NtSettings",
    props: ["file"],
    data() {
      return {
      }
    },
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
    mounted() {
      console.log(this.file)
    }
  }
</script>

<style scoped>
</style>