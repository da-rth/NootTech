<template>
    <main>
        <b-container class="bv-example-row" bg-variant="dark">
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