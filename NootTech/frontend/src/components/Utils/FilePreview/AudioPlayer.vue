<template>
  <div class="audioplayer">

    <div id="waveform"></div>

    <div class="row audioplayer-controls">

      <div class="col-sm-4">
        <div class="row justify-content-center">
          <span class="timestamp">
              <font-awesome-icon icon="clock"/> &nbsp;
              {{ `${fancyTimeFormat(timestamp)} / ${fancyTimeFormat(file.file_audio_info.duration)}` }}
          </span>
        </div>
      </div>

      <div class="col-sm-4">
        <div class="row justify-content-center play-pause-controls">
          <b-button class="audioplayer-btn" @click="stepBackward">
            <font-awesome-icon icon="step-backward"/>
          </b-button>

          <b-button class="audioplayer-btn" @click="playPause">
            <font-awesome-icon v-if="paused" icon="play"/>
            <font-awesome-icon v-else icon="pause"/>
          </b-button>

          <b-button class="audioplayer-btn" @click="stepForward">
            <font-awesome-icon icon="step-forward"/>
          </b-button>
        </div>
      </div>

      <div class="col-sm-4">
        <div class="row justify-content-center">
          <button class="audioplayer-btn" @click="toggleMute">
            <font-awesome-icon v-if="muted" icon="volume-off"/>
            <font-awesome-icon v-else icon="volume-up"/>
          </button>
          &nbsp;
          <input class="form-control-range volume-slider" type="range" min="0" max="1" step="0.01" value="0.7" v-model="volume"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import WaveSurfer from 'wavesurfer.js';
  import CursorPlugin from '../../../assets/js/wavesurfer.cursor.js';
  export default {
    name: "AudioPlayer",
    props: ['file'],
    modal: {
      prop: 'file',
      event: 'input'
    },
    data () {
      return {
        timestamp: 0,
        paused: true,
        muted: false,
        volume: 0.7,
        rate: 1,
        waveOptions: {
          container: '#waveform',
          waveColor: this.$root.colour,
          cursorColor: '#484848',
          progressColor: '#AAAAAA',
          autoCenter: true,
          barGap: 3,
          responsive: true,
          barHeight: 0.5,
          barWidth: 2,
          skipLength: 5,
          plugins: [ CursorPlugin.create({}) ]
        }
      }
    },
    computed: {
      // TODO: Possible LFI attacks?
      audioURL : function () {
        return this.file.file_content.startsWith('/') ? this.$backend_url+this.file.file_content : this.file.file_content;
      }
    },

    watch: {
      audio (newAudio) {
        this.resetPlayer(newAudio.file)
      },
      volume (val) {
        this.wavesurfer.setVolume(val);
      }
    },
    mounted () {
      this.wavesurfer = WaveSurfer.create(this.waveOptions);
      this.resetPlayer(this.audioURL);
      // Initialise events
      this.wavesurfer.on('audioprocess', () => {
        this.timestamp = parseInt(this.wavesurfer.getCurrentTime());
      });
      this.wavesurfer.on('finish', () => {
        this.paused = true;
        this.wavesurfer.setCurrentTime(0);
        this.timestamp = 0
      });
},
    methods: {
      playPause () {
        this.paused = !this.paused;
        this.wavesurfer.playPause()
      },
      toggleMute () {
        this.muted = !this.muted;
        this.wavesurfer.toggleMute();
      },
      stepForward () {
        this.wavesurfer.skipForward()
      },
      stepBackward () {
        this.wavesurfer.skipBackward()
      },
      resetPlayer(file) {
        this.volume = 0.7;
        this.paused = true;
        this.timestamp = 0;
        this.wavesurfer.pause();
        this.wavesurfer.empty();
        this.wavesurfer.load(file);
        this.wavesurfer.setVolume(this.volume);
      },
      setVolume (val) {
        this.wavesurfer.setVolume(val);
      },
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
    },
    beforeDestroy() {
      this.wavesurfer.pause();
      this.wavesurfer.destroy();
    },
  }
</script>

<style scoped>
    * {
      color: white;
    }
    .timestamp {
        padding-top: 2px;
        font-size: 14px;
    }

    .play-pause-controls {
      margin: -5px 0px 3px 0px;
    }

    .audioplayer-btn {
        background-color: transparent;
        color: rgba(255,255,255,0.8);
        border: none;
        font-size: 14px;
        outline:none;
        border: 0;
    }
    .audioplayer-btn:active,
    .audioplayer-btn:focus {
        outline:none;
        border: 0;
    }
    .audioplayer-btn:hover {
        cursor: pointer;
    }
    .audioplayer-controls {
        background-color: rgba(0,0,0,0.05);
        border-radius: 4px;
        padding: 5px;
        margin-bottom: -10px;
        border: 1px solid rgba(0,0,0,0.5);
        padding: 10px 0px 0px 0px;
    }
    .volume-slider {
        -webkit-appearance: none;
        width: 60px;
        margin: 7px 0px 7px 5px;
        height: 6px;
        background: #484848;
        outline: none;
        opacity: 0.8;
        -webkit-transition: .2s;
        transition: opacity .2s;
        border-radius: 10px;
    }
    .volume-slider:hover {
        opacity: 1;
    }
    .volume-slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 8px;
        height: 8px;
        background: #fff;
        cursor: pointer;
        border-radius: 100px;
    }
    .volume-slider::-moz-range-thumb {
        width: 8px;
        height: 8px;
        background: #fff;
        cursor: pointer;
    }

    #waveform wave {
      overflow-x: hidden;
    }
</style>
