<template>

  <div class="file-panel justify-content-center">

    <notifications group="FileDeletion" />

    <b-navbar toggleable="lg" type="dark" class="file-menubar">

      <b-navbar-toggle target="nav_file_collapse" />

      <b-collapse is-nav id="nav_file_collapse">

        <div class="col-md">

          <b-button-group>
            <b-button class="filebar-btn"><font-awesome-icon icon="minus"/></b-button>
            <b-button class="filebar-btn"><font-awesome-icon icon="plus"/></b-button>
          </b-button-group>

          <!-- Popup modal here? -->
          <b-button-group>
            <b-button class="filebar-btn"><font-awesome-icon icon="th"/></b-button>
            <b-button class="filebar-btn"><font-awesome-icon icon="list"/></b-button>
          </b-button-group>
          &nbsp;

          <a v-on:click="showPrivateFiles = !showPrivateFiles" name="check-button">
              <font-awesome-icon icon="share" v-if="showPrivateFiles"/>
              <font-awesome-icon icon="user-secret" v-else/>
              {{ showPrivateFiles ? "&nbsp;View Public files" : "&nbsp;View Private Files" }}
            </a>

          <b-button class="filebar-btn" variant="danger" v-if="selectFiles" v-on:click="deleteSelectedFiles()">Delete {{ selectedFiles.length }} file(s)</b-button>
          <b-button class="filebar-btn" variant="primary" v-if="selectFiles" v-on:click="privateSelectedFiles()">Make {{ selectedFiles.length }} file(s) private</b-button>

          <b-dropdown text="File List" v-if="selectedFiles.length > 0 && selectFiles">
            <b-dropdown-item v-bind:key="file.id" v-for="file in getCheckedFiles()" disabled>
              {{ file.generated_filename }} | {{ file.original_filename }}
            </b-dropdown-item>
          </b-dropdown>

        </div>

        <b-form-checkbox class="select-files-switch" switch v-model="selectFiles" name="check-button">
          Select Files
        </b-form-checkbox>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">

          <div class="col-sm">
            <input v-model="searchTerm" class="form-control file-search" type="search" :icon="['fas', 'search']" placeholder="Search..." aria-label="Search">
          </div>

          <div class="col-sm">

            <select @change="changedSelectionValue" class="custom-select file-sort">

              <option value="-date">Upload date (Latest)</option>
              <option value="date">Upload date (Oldest)</option>

              <option value="original_filename">Original Filename (A-Z)</option>
              <option value="-original_filename">Original Filename (Z-A)</option>

              <option value="generated_filename">Generated Filename (A-Z)</option>
              <option value="-generated_filename">Generated Filename (Z-A)</option>

              <option value="file_ext">Extension (Ascending)</option>
              <option value="-file_ext">Extension (Descending)</option>

              <option value="-views">Views (Most)</option>
              <option value="views">Views (Least)</option>
            </select>

          </div>

        </b-navbar-nav>

      </b-collapse>

    </b-navbar>

    <paginate name="searched_files" :list="$parent.searched_files" :per="paginate_by" tag="div" class="row file-row">

      <b-form-checkbox-group v-model="selectedFiles">

        <b-row class="file-grid justify-content-center">
          <template v-if="paginated('searched_files').length <= 0">
            <h1>You haven't uploaded any files yet! <font-awesome-icon icon="sad-tear"/></h1>
          </template>
          <template v-else>
            <template v-for="file in  paginated('searched_files')">
              <template v-if="showPrivateFiles">
                <NtBadge
                  class="file-badge"
                  v-if="file.is_private"
                  :key="file.id" :value="file"
                  :selectionStatus="selectFiles"
                  :selected="isSelected(file.id)"
                /></template>
              <template v-else><NtBadge
                class="file-badge"
                v-if="!file.is_private"
                :key="file.id" :value="file"
                :selectionStatus="selectFiles"
                :selected="isSelected(file.id)"
              /></template>
            </template>
          </template>

        </b-row>

      </b-form-checkbox-group>

    </paginate>

    <paginate-links
      class="file-pagination"
      for="searched_files"
      :hide-single-page="true"
      :classes="{'ul': 'pagination', 'li': 'page-item', 'a' : 'page-link'}"
      :show-step-links="true"
      :step-links="{next: 'Next', prev: 'Previous'}"
      >
    </paginate-links>

  </div>
</template>

<script>
  /**
   * MODAL currently broken by setting .file-grid "overflow: scroll". Perhaps because modal is inside badge component...
   */
  import NtBadge from "../Utils/Badge";
  import NtPopupModal from "../Utils/FilePopupModal"

  export default {
    name: "FilePanel",
    components: {NtBadge},
    data() {
      return {
        searchTerm: null,
        selectedFiles: [],
        selectFiles: false,
        showPrivateFiles: false,
        showUploadKey: false,
        checkFilesDeletion: false,
        checkFilesPrivate: false,
        paginate: ['searched_files'],
        page: {},
        paginate_by: 60,
      }
    },
    watch: {
      searchTerm: function (val) {
        if (val.length !== 0) {
          this.searchArray(val.toLowerCase(), this.$parent.files)
        } else {
          this.$parent.searched_files = this.$parent.files
        }
      }
    },



    methods: {

      async deleteSelectedFiles() {
        let deleteCount = 0;

        for (var i = 0; i < this.selectedFiles.length; i++) {
          // Make api call to delete file
          await this.$api.DeleteFile(this.selectedFiles[i])
          .then(response => {
            console.log('DELETE SUCCESS', response);
            // Increment delete count by 1
            deleteCount += 1;
            // Remove id from selectedFiles
            this.selectedFiles.splice(i, 1);

          })
          .catch(e => {
            // Catch the error and notify user that file cant be deleted
            console.log('ERROR', e.response);
            console.log("Could not delete file...")
            return null
          });
        }
        console.log(`Removed ${deleteCount} files...`);
        await this.$parent.loadFiles()
        this.$notify({
          group: 'FileDeletion',
          title: `Removed <strong>${deleteCount}</strong> files...`,
          text: 'The file panel is now updating...',
          position: 'bottom right'
        });
      },

      privateSelectedFiles() {
        console.log(`Attempting to privatise  ${this.selectedFiles.length} files`)
      },

      /** Used for "sort by" dropdown **/
      changedSelectionValue: function(item) {
        let value = item.target.value;
        if (value !== 'default') {
          this.$parent.searched_files = this.$parent.files.sort(this.dynamicSort(value));
          console.log(this.$parent.files)
        }
      },

      dynamicSort(property) {
        var sortOrder = 1;
        if(property[0] === "-") {
          sortOrder = -1;
          property = property.substr(1);
        }
        return function (a,b) {
          var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
          return result * sortOrder;
        }
      },

      /** Used for "search" input **/
      searchArray: function (term, array) {
        console.log(term)
        var results = [];
        for (var i=0; i < array.length; i++) {
          var has_gen_name = array[i].generated_filename.toString().toLowerCase().includes(term);
          var has_orig_name = array[i].original_filename.toString().toLowerCase().includes(term);
          var has_ext = array[i].file_ext.toString().toLowerCase().includes(term);
          if (has_gen_name | has_orig_name | has_ext) {
            results.push(array[i])
          }
        }
        if (results.length > 0) {
          this.$parent.searched_files = results;
        } else {
          this.$parent.searched_files = this.$parent.files
        }
      },

      getCheckedFiles() {
        let files = this.$parent.files.filter(f => this.selectedFiles.includes(f.id));
        console.log(files)
        return files
      },

      isSelected(file_id) {
        return this.selectedFiles.includes(file_id)
      }
    }
  }

</script>

<style scoped>
  * {
    color: #b8b8b8;
  }

  .file-panel {
    margin: 20px auto;
    height: 90vh;
    width: 90vw;
  }

  .file-menubar,
  .file-grid {
    padding: 10px;
    width: 92.2vw;
    margin: 20px -14px;
    border: 1px solid #121212;
    background-color: #1e1e1e !important;
  }

  .file-grid {
    height: auto;
    max-height: 74vh;
    overflow: scroll;
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

  .filebar-search {
    width: 15vw;
    font-size: 12px;
  }

  .file-badge {
    margin: 5px;
    height: 10rem;
    width: 18rem;
  }

  .file-search, .file-sort {
    background-color: rgba(0,0,0,0.2);
    border: 1px solid #3d3d3d;
  }

</style>
