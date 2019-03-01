<template>
    <b-card :key="file.id" no-body class="overflow-hidden row-card" :style="{height: height+'rem'}">
        <b-row no-gutters>
        <b-col md="2">
            <b-card-img :src="file.file_content" class="rounded-0" />
        </b-col>
        <b-col md="10">
            <b-card-body :title="file.original_filename">
            <b-card-text>
                This is a wider card with supporting text as a natural lead-in to additional content.
                This content is a little bit longer.
            </b-card-text>
            </b-card-body>
        </b-col>
        </b-row>
    </b-card>
</template>

<script>
export default {
    name: "RowBadge",
    props: ['file', 'height'],
}
</script>

<style>
  .row-card {
    width: 100%;
    margin: 5px;
    border: 1px solid rgba(255,255,255,0.1);
    background-color: rgba(0,0,0,0.1);
  }
</style>
