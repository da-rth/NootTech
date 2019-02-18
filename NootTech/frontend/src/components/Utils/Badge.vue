<template>
    <div v-bind:value="value" v-on:input="$emit('input', $event.target.value)">
        <NtImageBadge v-if="isImage" v-model="value" :selected=false />
    </div>
</template>

<script>
    import NtImageBadge from './ImageBadge.vue';

    export default {
        name: "NtBadge",
        components: {NtImageBadge},
        props: ['value'],
        methods: {
            isImage() {
                return this.value.file_mime_type.startsWith("image/")
            }
        }
    }
</script>
