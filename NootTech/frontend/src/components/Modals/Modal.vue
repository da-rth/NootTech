<template>
  <div v-if="$store.state.user && $store.state.settings">
    <nt-upload-modal />
    <nt-file-popup-modal />
    <nt-favourites-modal />
    <nt-settings-modal />
  </div>
</template>

<script>

import NtUploadModal from './UploadModal.vue';
import NtFilePopupModal from './FilePopupModal.vue';
import NtFavouritesModal from './FavouritesModal.vue';
import NtSettingsModal from './SettingsModal.vue';

export default {
  name: 'NtModal',
  components: {
    NtUploadModal,
    NtFilePopupModal,
    NtFavouritesModal,
    NtSettingsModal
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
