<template>
    <b-container fluid class="bv-example-row bg-dark">
        <b-form-row>
            <main>
                <slot></slot>
            </main>
        </b-form-row>
        <nt-footer></nt-footer>
    </b-container>
</template>
<script>
    import NtFooter from "./Footer.vue";

    export default {
        name: "NtMainPane",
        props: ["title"],
        created: function() {
            document.title = this.title
        },
        components: {NtFooter}
   }
</script>