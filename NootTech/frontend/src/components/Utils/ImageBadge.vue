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
        v-on:input="$emit('input', $event.target.value)"
        :img-src="value.thumbnail"
    >
        <div class="overlay">
			<h2>{{value.original_filename}}</h2>
			<div class="overlay-footer">
				<font-awesome-icon :icon="getIcon()"/>
			</div>
        </div>
    </b-card>
</template>

<script>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

  export default {
    name: "NtImageBadge",
    props: ["value", "selected"],
    components: {FontAwesomeIcon},
    methods: {
		getIcon() {
			// split into prefix and second name
			let src_icon = this.value.icon.split(" ")
			// it seems fontawesome is not happy with the fa-prefix
			src_icon[1] = src_icon[1].replace(/^fa-/gi, "");

			return src_icon
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
	bottom: 0;
	padding-left: 0.5em;
	padding-bottom: 0.2em;
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