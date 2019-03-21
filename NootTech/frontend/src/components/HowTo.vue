<template>

  <div id="HowTo" >
    <h1 class="centered">Uploading to NootTech</h1>
    <br/>
    <img class="upload-img" :src="$backend_url+'/media/upload.gif'">

    <br/><br/>
    <div class="centered">Just follow the steps above! Its as easy as that!</div>
    <br/><br/>

    <h1>Uploading through the command-line</h1>
    <p class="description">
      You can upload any of your files directly through the command-line using protocol software such as
      <a href="https://curl.haxx.se/">cURL</a>.
    </p>
    <highlight-code lang="bash">
    # You can upload files using cURL

    $ curl
    -F "username=Your_Username_Here"
    -F "upload_key=Your_Key_Here"
    -F "content=@/path/to/my/file.jpg"
    -F "content=@/path/to/my/second-file.jpg"
    {{ this.$site_url }}/api/upload
		</highlight-code>

    By running the above command, cURL should return the direct link to your newly uploaded file.
    <br/>
    Isn't that awesome? The possibilities are endless! <font-awesome-icon icon="surprise"/>
    <br/><br/>

    <h1>Uploading via ShareX</h1>
    <p class="description">
      <a href="https://getsharex.com/">ShareX</a> is a screen capturing, file sharing and productivity tool which can be used to upload your files and screenshots directly here!
      <br/></br/>
      To configure your ShareX application to upload to NootTech:
      <ul>
      <li>copy the <strong>code below</strong> to your clipboard</li>
      <li>right click the ShareX icon in your system tray</li>
      <li>Go to destinations... Custom Uploader Settings</li>
      <li>Click 'import' from Clipboard. This will fill the page with information.</li>
      <li>Update the username, upload_key and is_private fields with your information.</li>
      <li>Click 'Test Image Upload' to see if it works. If so, close the window</li>
      <li>Right click the ShareX icon again, Destination Settings...</li>
      <li>Change default Image Uploader and File Uploader to 'Custom Image/File Uploader'</li>
      </ul>
      And you are done! All of your screenshots/uploads should go straight to Noot.Tech!
      <br/><br/>
      <h4>ShareX configuration</h4>
    </p>
        <highlight-code lang="json">
    {
      "Version": "12.4.1",
      "Name": "NootTech",
      "DestinationType": "ImageUploader, FileUploader",
      "RequestMethod": "POST",
      "RequestURL": "https://noot.tech/api/upload",
      "Body": "MultipartFormData",
      "Arguments": {
        "username": "YOUR_USERNAME",
        "upload_key": "YOUR_UPLOAD_KEY",
        "is_private": false
      },
      "FileFormName": "content"
    }
    </highlight-code>
    <br/>
  </div>
</template>

<script>
  export default {
    name: "HowTo"
  }
</script>

<style>
#HowTo {
  margin: 0 auto;
  width: 84vw;
  height: 84vh;
  margin-top: 30px;
  padding: 30px;
}
.description {
  color: white;
}
.upload-img {
  width: 100%;
  border: 1px solid #858585;
}
.centered {
  text-align: center;
}
</style>
