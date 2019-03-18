<template>
  <div v-if="$store.state.user && $store.state.settings">
    <!-- Upload File modal -->
    <nt-upload-modal ref="uploadModal" />
    <nt-file-popup-modal ref="filePopupModal" />
    <nt-favourites-modal ref="favouritesPopupModal" />
  </div>
</template>

<script>

import NtUploadModal from './UploadModal.vue';
import NtFilePopupModal from './FilePopupModal.vue';
import NtFavouritesModal from './FavouritesModal.vue';
import EventBus from '../../event-bus.js';

export default {
  name: 'NtModal',
  components: {
    NtUploadModal,
    NtFilePopupModal,
    NtFavouritesModal
  },
}
</script>

<style scoped>
.privacy-switch {
  text-align: center;
  margin: 0 auto;
  padding: 5px;
}

.upload-form {
  margin: 30px 0;
}

.file-selection-area {
  overflow-y: hidden;
  height: 35px;
  border-radius: 5px;
}
</style>
