<template>
    <b-card
        overlay
        img-alg="Image"
        img-top
        tag="article"
        style="max-width: 20rem;"
        class="mb-2 hovereffect"
        :border-variant="selected ? 'primary' : 'white'"
        v-bind:value="value"
        text-variant="dark"
        v-on:input="$emit('input', $event.target.value)"
        :img-src="value.thumbnail"
    >
        <div class="overlay">
            <h2>{{value.original_filename}}</h2>
        </div>
    </b-card>
</template>

<script>
  export default {
    name: "NtImageBadge",
    props: ["value", "selected"],
    methods: {
        getThumbnail() {
            let src_thumnail = this.value.thumbnail
            
        }
    },
    created() {
        console.log(this.selected)
    }
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
    /**background-color: rgba(0,0,0,0.5);*/
    -webkit-transition: all .4s ease-in-out;
    transition: all .4s ease-in-out;
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
/*.hovereffect {
    width: 100%;
    height: 100%;
    float: left;
    overflow: hidden;
    position: relative;
    text-align: center;
    cursor: default;
}
.hovereffect .overlay {
    width: 100%;
    height: 100%;
    position: absolute;
    overflow: hidden;
    top: 0%;
    left: 0%;
    opacity: 0%;
    background-color: rgba(0,0,0,0.5);
    -webkit-animation:all .4s ease-in-out;
    transition:all .4s ease-in-out;
}

.hovereffect img {
    display: block;
    position: relative;
    -webkit-transition: all .4s linear;
    transition: all .4s linear;
}

.hovereffect h2 {
    text-transform:uppercase;
    /*color:#fff;
    text-align:center;
    position:relative;
    font-size:17px;
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
    filter:alpha(opacity=100);
}

.hovereffect:hover h2,.hovereffect:hover a.info {
    opacity:1;
    filter:alpha(opacity=100);
    -ms-transform:translatey(0);
    -webkit-transform:translatey(0);
    transform:translatey(0);
}


*/
</style>