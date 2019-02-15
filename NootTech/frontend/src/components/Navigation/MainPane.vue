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
        data: function() {
            return {
                dummy: 42
            }
        }
    }
</script>