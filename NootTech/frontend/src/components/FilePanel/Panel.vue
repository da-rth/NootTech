<template>
  <div>
        <h4 v-for="file in $parent.files" style="color: white">
          {{ file.generated_filename}} - {{ file.date }}
        </h4>
  </div>
</template>

<script>

  export default {
    name: "FilePanel",
  }
</script>

<style>
    .file-views {
        opacity: 0;
        position: absolute;
        left: 5px;
        top: 5px;
        background-color: #3d3d3d;
        padding: 1px 6px;
        border-radius: 2px;
        font-size: 11px;
        user-select: none;
        transition: opacity 0.2s ease-in-out;
        border: 1px solid #FFFFFF11;
    }
    .file-href:hover .file-views {
        opacity: 1;
    }
    .file-label {
        width: 120px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .delete-alert {
        text-align: center;
        margin-top: 5px;
        margin-bottom: -5px;
        background-color: #242424;
    }
    .deletion-border {
        border: 1px solid red !important;
    }
    .thumbnail-play {
        color: #d0d0d0;
        position: absolute;
        font-size: 2em;
        width: 100%;
        margin-top: 18.5%;
        pointer-events: none;
        transition: color 0.2s ease-in-out;
        opacity: 0.95;
        text-shadow: 0 0 2px #000000;
    }
    .file-block {
        position: relative;
    }
    .file-block:hover .thumbnail-play {
        color: #FFF;
        opacity: 0.9;
    }
    .file-label {
        transition: color 0.2s ease-in-out;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .file-block:hover .file-label {
        color: #00cccc;
        cursor: pointer;
    }
    .col-fb-lg .file-awesome {
        font-size: 3.9em;
        padding-top: 7%;
    }
    .col-fb-md .file-awesome {
        font-size: 3em;
        padding-top: 7%;
    }
    .col-fb-sm .file-awesome {
        font-size: 2.5em;
        padding-top: 7%;
    }
    .file-row {
        padding-top: 20px;
    }
    /* Image Thumbnail */
    .img-thumbnail {
        background-color: rgba(0,0,0,0.4) !important;
        cursor: pointer;
        transition: border 0.2s ease-in-out;
    }
    .normal-border {
        border: 1px solid black !important;
    }
    .normal-border:hover {
        border: 1px solid rgba(144, 144, 144, 0.6) !important;
    }
    /* Scrollbar */
    .container-fluid.file-container::-webkit-scrollbar {
        width: 8px;
    }
    .container-fluid.file-container::-webkit-scrollbar-track {
        box-shadow: none;
    }
    .container-fluid.file-container::-webkit-scrollbar-thumb {
        background: transparent;
        border-radius: 3px;
    }
    .container-fluid.file-container:hover::-webkit-scrollbar-thumb {
        background: #3d3d3d;
        border-radius: 3px;
    }
    .col-fb-lg,
    .col-fb-md,
    .col-fb-sm {
        margin: 5px;
        transition: all 0.4s ease-in-out;
    }
    .col-fb-lg .file-label {
        font-size: 15px;
    }
    .col-fb-md .file-label {
        font-size: 14px;
    }
    .col-fb-sm .file-label {
        font-size: 12px;
    }
    @media (max-width: 576px) {
        .col-fb-lg {
            width: 93%;
        }
        img.img-fluid.img-thumbnail.file-thumb {
            width: 100%;
        }
        .col-fb-md {
            width: 45%;
        }
        .col-fb-sm {
            width: 29.5%;
        }
        .row.file-row {
            margin-left: 1%;
        }
    }
    @media (min-width: 576px) {
        .col-fb-lg {
            width: 46%;
        }
        img.img-fluid.img-thumbnail.file-thumb {
            width: 100%;
        }
        .col-fb-md {
            width: 30%;
        }
        .col-fb-sm {
            width: 22%;
        }
        .row.file-row {
            margin-left: 1%;
        }
    }
    /*Medium devices (tablets, 768px and up)*/
    @media (min-width: 768px) {
        .col-fb-lg {
            width: 23%
        }
        .col-fb-md {
            width: 18%
        }
        .col-fb-sm {
            width: 15%
        }
        .row.file-row {
            margin-left: 10px;
        }
    }
    /*Large devices (desktops, 992px and up)*/
    @media (min-width: 992px) {
        .col-fb-lg {
            width: 18.3%
        }
        .col-fb-md {
            width: 15%
        }
        .col-fb-sm {
            width: 11%
        }
        .row.file-row {
            margin-left: 20px;
        }
    }
    /*Extra large devices (large desktops, 1200px and up)*/
    @media (min-width: 1200px) {
        .col-fb-lg {
            width: 15.5%;
        }
        .col-fb-md {
            width: 10.1%;
        }
        .col-fb-sm {
            width: 8.1%;
        }
        .row.file-row {
            margin-left: 2%;
        }
    }
    /*Extra extra large devices (extra large desktops, 1920px and up)*/
    @media (min-width: 1920px) {
        .col-fb-lg {
            width: 13.5%;
        }
        .col-fb-md {
            width: 10.4%;
        }
        .col-fb-sm {
            width: 8.45%;
        }
        .row.file-row {
            margin-left: 1.5%;
        }
        .file-label {
            font-size: 18px !important;
        }
    }
    .file-thumb {
        object-fit: contain;
        padding: 1px;
        border-radius: 2px;
        border: none;
        transition: background-color 0.1s ease-in-out;
        height: 79.8%;
    }
    .file-delete-checkbox {
        display: none;
        position: absolute;
        right: 5px;
        top: 5px;
        opacity: 0.7;
        transition: opacity 0.2s ease-in-out;
    }
    .file-block:hover .file-delete-checkbox {
        opacity: 1;
    }
</style>
