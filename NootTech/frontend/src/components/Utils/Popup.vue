<!-- The Popup component is a mere wrapper of the Modal component
     of Bootstrap-vue, with proper styling and formatting. -->
<template>
    <div>
        <b-modal v-bind:id="id" v-bind:title="title">
            <p class="my-4">
                <slot></slot>
            </p>
        </b-modal>
    </div>
</template>
<script>
    export default {
        name: "NtPopup",
        props: ["title", "id"],
        methods: {
            showModal () {
                this.$root.$emit('bv::show::modal',this.id)
            },
            hideModal () {
                this.$root.$emit('bv::hide::modal',this.id)
            }
        }
   }
</script>