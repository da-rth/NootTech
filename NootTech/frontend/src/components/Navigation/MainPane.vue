<template>
    <main>
        <b-container fluid class="bv-example-row bg-dark">
            <b-form-row>
                <slot></slot>
            </b-form-row>
        </b-container>
    </main>
</template>
<script>
    export default {
        name: "NtMainPane",
        props: ["title"],
        created: function() {
            document.title = this.title

        }
   }
</script>