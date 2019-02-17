<template>
  <div class="loading-container">
    <H1 class="loading-header">{{ multiple === true ? 'Collecting your files...' : 'Loading page...' }}</H1>
    <!-- svg by https://www.vexels.com/png-svg/preview/138470/dog-pug-silhouette -->
    <br/>
    <div class="lds-ring"><div></div><div></div><div></div><div></div></div>

  </div>
</template>

<script>
export default {
  name: "LoadingFiles",
  components: {
  },
  props: ['multiple']
}
</script>

<style scoped>
  .loading-container {
    text-align: center;
    margin-left: 10%;
    margin-right: 10%;
    margin-top: 70px;
  }
  .loading-container .loading-header {
    font-family: 'Source Sans Pro', sans-serif;
  }
  .lds-ring {
    display: inline-block;
    position: relative;
    width: 50px;
    height: 50px;
    opacity: 0.3;
  }
  .lds-ring div {
    box-sizing: border-box;
    display: block;
    position: absolute;
    width: 40px;
    height: 40px;
    margin: 4px;
    border: 4px solid #fff;
    border-radius: 50%;
    animation: lds-ring 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    border-color: #fff transparent transparent transparent;
  }
  .lds-ring div:nth-child(1) {
    animation-delay: -0.45s;
  }
  .lds-ring div:nth-child(2) {
    animation-delay: -0.3s;
  }
  .lds-ring div:nth-child(3) {
    animation-delay: -0.15s;
  }
  @keyframes lds-ring {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
