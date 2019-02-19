<template>
  <b-card
    overlay
    img-alg="Image"
    img-top
    tag="article"
    style="width: 18rem;"
    class="mb-2 hovereffect"
    :border-variant="selected ? 'primary' : 'white'"
    v-bind:value="value"
    text-variant="dark"
    v-on:input="$emit('input', $event.target.value); "
    :img-src="value.file_thumbnail"
  >
    <nt-image-badge :ref="popup_id" v-if="isImage()" v-model="value" />

    <b-form-checkbox class="badge-checkbox" v-if="selectionStatus" v-bind:value="value.id"></b-form-checkbox>

    <div class="overlay" v-else @click="showModal">
      <b-form-checkbox class="badge-checkbox" v-if="selectionStatus" v-bind:value="value.id"></b-form-checkbox>
      <h2>{{value.original_filename}}</h2>
      <div class="overlay-footer">
        <div class="icon">
          <font-awesome-icon :icon="getIcon()"/>
        </div>
        <div class="views">
          <font-awesome-icon icon="eye"/>
          <span style="padding-left: 2px">{{getViews()}}</span>
        </div>
      </div>
    </div>
  </b-card>
</template>

<script>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import NtImageBadge from './ImageBadge.vue';
  export default {
    name: "NtBadge",
    components: {NtImageBadge, FontAwesomeIcon},
    props: ['value', 'selected', 'selectionStatus'],
    data() {
      return {
        popup_id: 'popup-' + this.value.id,
        isSelected: this.selected ? true : false // get rid of vue's warning
      }
    },
    methods: {
      showModal() {
        this.$refs[this.popup_id].showModal();
      },
      selectionIsOn() {
        return this.$parent.selectFiles;
      },
      isImage() {
        return this.value.file_mime_type.startsWith("image/")
      },
      getIcon() {
        // split into prefix and second name
        let src_icon = this.value.icon.split(" ")
        // it seems fontawesome is not happy with the fa-prefix
        src_icon[1] = src_icon[1].replace(/^fa-/gi, "");
        return src_icon
      },
      getViews() {
        let views = this.value.views;
        if (views > 1e6)
          return (views / 1e6).toFixed(1) + "M";
        if(views > 1000)
          return (views / 1e3).toFixed(1) + "K";
        return views;
      }
    },
  }
</script>

<style scoped>
  .hovereffect {
    overflow: hidden;
    display: inline-block;
  }
  .hovereffect .overlay {
    width: 100%;
    height: 100%;
    position: absolute;
    overflow: hidden;
    display: inline-block;
    top: 0;
    left: 0;
    opacity: 0;
    background-color: rgba(0,0,0,0.5);
    -webkit-transition: all .4s ease-in-out;
    transition: all .4s ease-in-out;
  }
  .overlay-footer {
    background: rbga(0, 0, 0, 0.6);
    color: lightgray;
    position: absolute;
    width: 100%;
    bottom: 0;
    padding: 0 0.5em 0.2em;
  }
  .icon {
    float: left;
  }
  .views {
    float:right;
  }
  .hovereffect:hover {
    cursor: pointer;
  }
  .hovereffect h2 {
    text-transform: uppercase;
    text-align: center;
    position: relative;
    font-size: 0.7em;
    color: lightgray;
    background:rgba(0,0,0,0.6);
    -webkit-transform:translatey(-100px);
    -ms-transform:translatey(-100px);
    transform:translatey(-100px);
    -webkit-transition:all .2s ease-in-out;
    transition:all .2s ease-in-out;
    padding:10px;
  }
  .hovereffect:hover img {
    -ms-transform:scale(1.2);
    -webkit-transform:scale(1.2);
    transform:scale(1.2);
  }
  .hovereffect:hover .overlay {
    opacity:1;
    filter: alpha(opacity=100)
  }
  .hovereffect:hover h2 {
    opacity: 1;
    filter: alpha(opacity=100);
    -ms-transform:translatey(0);
    -webkit-transform:translatey(0);
    transform: translatey(0);
  }

</style>
