<template>

    <div id="FileInformation">
        <table class="info-table">

            <tr>
                <td><strong>Original Filename:</strong></td>
                <td>{{ file.original_filename }}</td>
            </tr>

            <tr>
                <td><strong>Generated Filename:</strong></td>
                <td>{{ file.generated_filename }}{{ file.file_ext}}</td>
            </tr>

            <tr>
                <td><strong>Upload Date:</strong></td>
                <td>{{ date }}</td>
            </tr>

            <tr>
                <td><strong>File Size:</strong></td>
                <td>{{ file.file_size_str }}</td>
            </tr>

            <tr>
                <td><strong>Views:</strong></td>
                <td>{{ file.views }}</td>
            </tr>


            <template v-if="file.file_image_info">
                <tr>
                    <td><strong>Resolution:</strong></td>
                    <td>{{ file.file_image_info.resolution }}</td>
                </tr>
                <tr v-if="file.file_image_info.mode">
                    <td><strong>Mode:</strong></td>
                    <td>{{ file.file_image_info.mode }}</td>
                </tr>
                <br/>
            </template>

            <template v-if="file.file_video_info">
                <tr>
                    <td><strong>Resolution:</strong></td>
                    <td>{{ file.file_video_info.resolution }}</td>
                </tr>
                <tr>
                    <td><strong>Duration:</strong></td>
                    <td>{{ fancyTimeFormat(file.file_video_info.duration) }}</td>
                </tr>
                <tr>
                    <td><strong>FPS:</strong></td>
                    <td>{{ file.file_video_info.fps }}</td>
                </tr>
            </template>

            <template v-if="file.file_audio_info">
                <tr>
                    <td><strong>Duration:</strong></td>
                    <td>{{ fancyTimeFormat(file.file_audio_info.duration) }}</td>
                </tr>
                <tr>
                    <td><strong>Sample Rate:</strong></td>
                    <td>{{ file.file_audio_info.sample_rate }}</td>
                </tr>
            </template>

            <template v-if="file.file_text_info">
                <tr>
                    <td><strong>Lines:</strong></td>
                    <td>{{ file.file_text_info.lines }}</td>
                </tr>

                <tr>
                    <td><strong>Characters:</strong></td>
                    <td>{{ file.file_text_info.characters }}</td>
                </tr>
            </template>

        </table>
    </div>
</template>

<script>
export default {
    name: "FileInformation",
    props: ["file"],
    computed: {
        virusItems: function () {
          return [ { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' }];
        },
        date : function () {
            return  this.file.date.split(".")[0].split("T").join(" at ");
        }
    },
    methods: {
        fancyTimeFormat (time) {
            // From : https://stackoverflow.com/a/11486026
            // Hours, minutes and seconds
            var hrs = ~~(time / 3600);
            var mins = ~~((time % 3600) / 60);
            var secs = ~~time % 60;

            // Output like "1:01" or "4:03:59" or "123:03:59"
            var ret = "";

            if (hrs > 0) {
                ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
            }

            ret += "" + mins + ":" + (secs < 10 ? "0" : "");
            ret += "" + secs;
            return ret;
        }
    }
}
</script>

<style scoped>

#FileInformation {
    margin: 0 auto;
    background-color: rgba(0,0,0,0.2);
    padding: 20px;
    color: #ffffff;
    border: 1px solid #121212;
}
#FileInformation table {
    width: 40%;
    margin: 0 auto;

}
#FileInformation td {
  white-space: nowrap; 
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
}
.info-table {
    width: 100%;
}

</style>
