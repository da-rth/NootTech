<template>
  <div class="file-panel">
    <b-navbar toggleable="lg" type="dark" class="file-menubar">

      <b-navbar-toggle target="nav_file_collapse" />

      <b-collapse is-nav id="nav_file_collapse">

        <b-button-group>
          <b-button class="filebar-btn">Small</b-button>
          <b-button class="filebar-btn">Med</b-button>
          <b-button class="filebar-btn">Large</b-button>
        </b-button-group>

        <b-input-group prepend="K" class="filebar-uploadkey" v-if="showUploadKey">
          <b-form-input class="key-field" v-bind:value="$parent.settings.upload_key" readonly/>
          <b-input-group-append>
            <b-button>Copy</b-button>
          </b-input-group-append>
        </b-input-group>

        <b-form-checkbox class="select-files-switch" switch v-model="showUploadKey" name="check-button">
          {{ showUploadKey ? "Hide Key" : "Show Key" }}
        </b-form-checkbox>

        <b-form-checkbox class="select-files-switch" switch v-model="selectFiles" name="check-button">
          Select Files...
        </b-form-checkbox>

        <b-dropdown text="File List" v-if="selectedFiles.length > 0 && selectFiles">
          <b-dropdown-item v-for="file in getCheckedFiles()">
            {{ file.generated_filename }} | {{ file.original_filename }}
          </b-dropdown-item>
        </b-dropdown>


        <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2 filebar-search" type="text" placeholder="Search"/>
        </b-nav-form>

          <b-nav-item-dropdown right>
            <!-- Using button-content slot -->
            <template slot="button-content"><em>Filesize</em></template>
            <b-dropdown-item href="#">Image</b-dropdown-item>
            <b-dropdown-item href="#">Audio</b-dropdown-item>
            <b-dropdown-item href="#">Video</b-dropdown-item>
            <b-dropdown-item href="#">Text</b-dropdown-item>
            <b-dropdown-item href="#">Other</b-dropdown-item>
          </b-nav-item-dropdown>

          <b-nav-item-dropdown right>
            <!-- Using button-content slot -->
            <template slot="button-content"><em>Type</em></template>
            <b-dropdown-item href="#">Image</b-dropdown-item>
            <b-dropdown-item href="#">Audio</b-dropdown-item>
            <b-dropdown-item href="#">Video</b-dropdown-item>
            <b-dropdown-item href="#">Text</b-dropdown-item>
            <b-dropdown-item href="#">Other</b-dropdown-item>
          </b-nav-item-dropdown>

        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <paginate name="searched_files" :list="$parent.searched_files" :per="paginate_by" tag="div" class="row file-row">

      <b-form-checkbox-group v-model="selectedFiles">
        <b-row class="file-grid justify-content-center">
          <b-col v-bind:id="file.id" cols="1" lg="1" v-for="file in paginated('searched_files')" class="file-block" v-bind:style="{ 'background-image': 'url(' + file.file_thumbnail + ')' }">
            <b-form-checkbox v-if="selectFiles" v-bind:value="file.id" @change="changeBorder"></b-form-checkbox>
          </b-col>
        </b-row>
      </b-form-checkbox-group>

    </paginate>

    <paginate-links class="file-pagination" for="searched_files"
                    :hide-single-page="true"
                    :classes="{'ul': 'pagination', 'li': 'page-item', 'a' : 'page-link'}"
                    :show-step-links="true"
                    :step-links="{next: 'Next', prev: 'Previous'}">
    </paginate-links>

        <div class="text-center">
      Selected files: {{ selectedFiles }}
      <br/>
      <b-button class="filebar-btn" variant="danger" v-if="selectFiles">Delete files</b-button>
      <b-button class="filebar-btn" variant="primary" v-if="selectFiles">Make files private</b-button>
    </div>

  </div>
</template>

<script>

  export default {
    name: "FilePanel",

    data() {
      return {
        selectedFiles: [],
        selectFiles: false,
        showUploadKey: false,
        checkFilesDeletion: false,
        checkFilesPrivate: false,
        paginate: ['searched_files'],
        page: {},
        paginate_by: 60,
      }
    },
    methods: {
      changeBorder(checked) {
        // User can select files to either delete or set private, but not both at the same time.
        console.log(JSON.stringify(checked))
        /**
         if (this.checkFilesDeletion) {
          console.log("change border colour of file to red")
        } else if (this.checkFilesPrivate) {
          console.log("change border colour of file to blue")
        }
         */
      },
      getCheckedFiles() {
        let files = this.$parent.files.filter(f => this.selectedFiles.includes(f.id));
        console.log(files)
        return files
      },
    }
  }
</script>

<style scoped>
  * {
    color: #b8b8b8;
  }
  .file-panel {
    width: 92vw;
    height: 78vh;
    margin: 30px auto;
  }
  .file-menubar, .file-grid {
    margin-bottom: 20px;
    border: 1px solid #121212;
    background-color: #1e1e1e !important;
  }
  .file-grid {
    color: #9c9c9c;
    padding: 10px;
    max-height: 72vh;
    margin-bottom: 10px;
    overflow-y: scroll;
  }

  .file-block {
    margin: 10px;
    border-radius: 4px;
    background-size: cover;
    border: 1px solid #191919;
    width: auto;
    height: 100px;
  }

  .file-block:hover {
    border-color: #fff;
  }

  .file-checkbox-group {
    width: 100%;
    height: 100%;
  }

  .file-pagination {
    justify-content: center;
  }
  .select-files-switch {
    margin: 0px 7px;
  }
  .filebar-btn {
    margin: 0px 5px;
    height: 34px;
    padding: 5px 10px;
  }
  .filebar-uploadkey {
    width: 300px;
  }
  {
    font-size: 12px;
  }
  .filebar-uploadkey .btn,
  .filebar-uploadkey .input-group-text,
  .filebar-uploadkey .key-field {
    font-size: 12px;
  }

  .filebar-uploadkey .input-group-text,
  .filebar-uploadkey .key-field {
    color: #242424;
  }

  .filebar-search {
    width: 15vw;
    font-size: 12px;
  }

</style>
