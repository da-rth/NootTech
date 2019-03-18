<template>

  <div class="file-panel">
      {{action}}


    <notifications group="FileUpdate" />

    <b-navbar toggleable="lg" type="dark" class="file-menubar">
      <b-navbar-brand>Files</b-navbar-brand>
      <b-navbar-toggle target="nav_file_collapse" />

      <b-collapse is-nav id="nav_file_collapse">

        <div class="col d-flex justify-content-between">
          <b-button-group class="filebar-btn-group">
            <b-button class="filebar-btn" v-on:click="decreaseWH()"><font-awesome-icon icon="minus"/></b-button>
            <b-button class="filebar-btn" v-on:click="increaseWH()"><font-awesome-icon icon="plus"/></b-button>
          </b-button-group>
        </div>

        <div class="col">
          <b-button class="file-panel-btn" v-on:click="showPrivateFiles = !showPrivateFiles" name="check-button">
              <font-awesome-icon icon="share" v-if="showPrivateFiles"/>
              <font-awesome-icon icon="user-secret" v-else/>
              {{ showPrivateFiles ? "&nbsp;View Public files" : "&nbsp;View Private Files" }}
            </b-button>
        </div>

        <div class="col">
          <b-button class="file-panel-btn file-selection-btn" v-on:click="selectFiles = !selectFiles">
            <font-awesome-icon icon="hand-pointer"/>&nbsp; <template v-if="selectFiles">Disable</template><template v-else>Enable</template> File Selection
          </b-button>
        </div>
        
        <div class="col">
          <b-button class="file-panel-btn" variant="danger" v-if="selectFiles" v-on:click="deleteSelectedFiles()" :disabled="selectedFiles.length < 1">Delete</b-button>
        </div>

        <div class="col">
          <b-button class="file-panel-btn" variant="primary" v-if="selectFiles" v-on:click="privateSelectedFiles()" :disabled="selectedFiles.length < 1">Toggle Privacy</b-button>
        </div>

        <div class="col">
          <b-dropdown text="File List" v-if="selectedFiles.length > 0 && selectFiles">
            <b-dropdown-item class="file-panel-btn" v-bind:key="file.id" v-for="file in getCheckedFiles()" disabled>
              {{ file.generated_filename }} | {{ file.original_filename }}
            </b-dropdown-item>
          </b-dropdown>
        </div>

        <div class="col-md-2">
          <input v-model="searchTerm" class="form-control file-panel-btn file-search" type="search" :icon="['fas', 'search']" placeholder="Search..." aria-label="Search">
        </div>

        <div class="col-md-1">
          <select @change="changedSelectionValue" class="custom-select file-panel-btn file-sort">
            <option class="opt" value="-date">Sorty by...</option>

            <option class="opt" value="-date">Upload date (Latest)</option>
            <option class="opt" value="date">Upload date (Oldest)</option>

            <option class="opt" value="original_filename">Original Filename (A-Z)</option>
            <option class="opt" value="-original_filename">Original Filename (Z-A)</option>

            <option class="opt" value="generated_filename">Generated Filename (A-Z)</option>
            <option class="opt" value="-generated_filename">Generated Filename (Z-A)</option>

            <option class="opt" value="file_ext">Extension (Ascending)</option>
            <option class="opt" value="-file_ext">Extension (Descending)</option>

            <option class="opt" value="-views">Views (Most)</option>
            <option class="opt" value="views">Views (Least)</option>

            <option class="opt" value="-file_size_bytes">Filesize (Largest)</option>
            <option class="opt" value="file_size_bytes">Filesize (Smallest)</option>
          </select>
        </div>
      </b-collapse>
    </b-navbar>

    <paginate name="searched_files" :list="$parent.searched_files" :per="paginate_by" tag="div" class="row file-row" v-if="$parent.searched_files">
      <b-row class="file-grid justify-content-center">
        <template v-if="paginated('searched_files').length <= 0">
          <h1>You haven't uploaded any files yet! <font-awesome-icon icon="sad-tear"/></h1>
        </template>

        <template v-else>
          <template v-for="file in  paginated('searched_files')">
            <template v-if="grid_view">
              <template v-if="showPrivateFiles">
                <NtBadge
                  :style="{
                    width: `${thumb_size.width}rem`,
                    height: `${thumb_size.height}rem`
                    }"
                  class="file-badge"
                  v-if="file.is_private"
                  :key="file.id" :value="file"
                  :selectionStatus="selectFiles"
                  :selected="isSelected(file.id)"/>
              </template>
              <template v-else>
                <NtBadge
                  :style="{
                    width: `${thumb_size.width}rem`,
                    height: `${thumb_size.height}rem`
                    }"
                  v-if="!file.is_private"
                  class="file-badge"
                  :key="file.id" :value="file"
                  :selectionStatus="selectFiles"
                  :selected="isSelected(file.id)"/>
              </template>
            </template>
            <template v-else>
              <template v-if="showPrivateFiles">
                <nt-row-badge :key="file.id" :height="row_height" :file="file" v-if="file.is_private"/>
              </template>
              <template v-else>
                <nt-row-badge :key="file.id" :height="row_height" :file="file"/>
              </template>
            </template>
          </template>
        </template>
      </b-row>
    </paginate>

    <paginate-links
      class="file-pagination"
      for="searched_files"
      :hide-single-page="true"
      :classes="{'ul': 'pagination', 'li': 'page-item', 'a' : 'page-link'}"
      :show-step-links="true"
      :step-links="{next: 'Next', prev: 'Previous'}"
      v-if="$parent.searched_files"
      >
    </paginate-links>

  </div>
</template>

<script>
  import * as types from '../../store/mutation-types.js';
  import NtBadge from "../Utils/Badge";
  import NtRowBadge from "../Utils/RowBadge"

  export default {
    name: "FilePanel",
    components: {NtBadge, NtRowBadge},
    data() {
      return {
        searchTerm: null,
        selectFiles: false,
        showPrivateFiles: false,
        showUploadKey: false,
        checkFilesDeletion: false,
        checkFilesPrivate: false,
        paginate: ['searched_files'],
        page: {},
        paginate_by: 60,
        thumb_size: {
          // rem
          width: 18,
          height: 10
        },
        row_height: 10,
        grid_view: true,
        openedFile: null
      }
    },
    computed: {
      action() {
        return this.$store.state.action;
      },
      selectedFiles() {
        return this.$store.state.selected_files;
      }
    },
    watch: {
      searchTerm: function (val) {
        if (val.length !== 0) {
          this.searchArray(val.toLowerCase(), this.$parent.files)
        } else {
          this.$parent.searched_files = this.$parent.files
        }
      },
      selectFiles: function (val) {
          this.$store.commit(types.EMPTY_FILE_SELECTION);
      }
    },



    methods: {

      increaseWH() {
        if (this.thumb_size.width < 28 && this.row_height < 18) {
          this.thumb_size.width += 0.5;
          this.thumb_size.height += 0.5;
          this.row_height += 0.5;
        }
      },
      decreaseWH() {
        if (this.thumb_size.width > 4 && this.row_height >= 7) {
          this.thumb_size.width -= 0.5;
          this.thumb_size.height -= 0.5;
          this.row_height -= 0.5;
        }
      },

      async deleteSelectedFiles() {

        let deleteCount = 0;

        for (var i = 0; i < this.selectedFiles.length; i++) {
          // Make api call to delete file
          await this.$api.DeleteFile(this.selectedFiles[i])
          .then(response => {
            console.log('DELETE SUCCESS', response);
            // Increment delete count by 1
            deleteCount += 1;
          })
          .catch(e => {
            // Catch the error and notify user that file cant be deleted
            console.log('ERROR', e);
          });
        }
        await this.$parent.loadFiles()
        this.$notify({
          group: 'FileUpdate',
          title: `Removed <strong>${deleteCount}</strong> files...`,
          text: 'The file panel is now updating...',
          position: 'bottom right'
        });
        this.$store.commit('EMPTY_FILE_SELECTION');
        this.$store.commit('REFRESH_FILE_PANEL', true);
      },

      async privateSelectedFiles() {
        let privateCount = 0;

        for (var i = 0; i < this.selectedFiles.length; i++) {

          await this.$api.TogglePrivacy(this.selectedFiles[i])
          .then(response => {
            console.log('TOGGLE PRIVACY SUCCESS', response);
            privateCount++;
          })
          .catch(e => {
            console.log('TOGGLE PRIVACY ERROR', e);
          });
        }

        await this.$parent.loadFiles()

        this.$notify({
          group: 'FileUpdate',
          title: `Toggled the privacy status of <strong>${privateCount}</strong> files...`,
          text: 'The file panel is now updating...',
          position: 'bottom right'
        });

        this.$store.commit('EMPTY_FILE_SELECTION');
        this.$store.commit('REFRESH_FILE_PANEL', true);
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
        return files
      },

      isSelected(file_id) {
        return this.selectedFiles.includes(file_id)
      }
    }
  }

</script>

<style>
  .file-panel {
    overflow: hidden !important;
  }
  * {
    color: #b8b8b8;
  }
  .filebar-btn-group {
    width: 100%;
  }
  .file-panel-btn {
    width: 100%;
    background-color: transparent !important;
    margin: 5px 0px;
    font-size: 14px;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  .file-selection-btn {
    padding: 7px 0px;
  }

  .file-panel {
    margin: 20px auto;
    max-height: 90vh;
    width: 90vw;
    overflow-x: hidden;
    overflow-y: auto;
  }

.file-menubar {
    width: 100%;
    background-color: rgba(0,0,0,0.1);
    padding: 3px;
    border: 1px solid #121212;
}

  .file-grid {
    padding: 10px;
    width: 92.2vw;
    margin: 20px -14px;
    border: 1px solid #121212;
    background-color: #1e1e1e !important;
  }
  .row {
      display: -ms-flexbox;
      display: flex;
      -ms-flex-wrap: wrap;
      flex-wrap: wrap;
      justify-content: center;
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
    background-color: transparent;
  }

  .file-search, .file-sort {
    background-color: rgba(0,0,0,0.2);
    border: 1px solid #555b60 !important;
  }

  .filebar-btn-group .filebar-btn {
    background-color: transparent;
    border: 1px solid #555b60;
    border-radius: 5px;
    margin: 5px 0px;
    padding: 10px;
    height: 40px;
  }

  .filebar-btn-group .filebar-btn:focus {
    border: none;
    box-shadow: none;
  }

  .filebar-btn-group {
    border: 1px solid #202020;
  }

  .opt {
    color: black;
  }
</style>
