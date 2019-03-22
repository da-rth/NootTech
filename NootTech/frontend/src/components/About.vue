<template>
  <div class="about-container">

    <div class="project-information" >
      
      <b-row>
        
        <b-col md="9">
        <h1>About NootTech...</h1>
        We built this website with the aim to incorporate an easy to use uploading system built for instant file sharing, and with the user’s privacy in mind.
        <br/><br/>
        As a NootTech user, you have are given the ability to upload your files off-site, through software such as cURL and ShareX. This allows for many possibilities, such as allowing advanced users to write their own upload scripts.
        <br/><br/>
        However, we strive to create a user-friendly, minimalistic and uncluttered website – ensuring the user is never overwhelmed with uncessary information. All communication to/from our website is encrypted using HTTPS, ensuring that all information is safely transferred between destinastions. 
        <br/><br/>
        <h4>Have questions? Contact us at: <a href="mailto:contact@noot.tech">contact@noot.tech</a> or checkout our Discord Server</h4>
        <br/>
      </b-col>
      
      <b-col md="3">
        <iframe class="discord-embed" src="https://discordapp.com/widget?id=558287009584513063&theme=dark" width="100%" height="300px" allowtransparency="true" frameborder="0"></iframe>
      </b-col>
      
      </b-row>
    
    

    <br/><br/>
    <h1 class="contributor-header">Contributors</h1>

    <b-row class="contrib-row">
      <b-col-md-3></b-col-md-3>
    <b-col-md-2 :key="contributor.id" v-for="contributor in myGitHubData.contributors">
        <a class="git-href" :href="contributor.html_url">
          <b-card
            v-if="contributor.html_url"
            :title="contributor.login"
            :img-src="contributor.avatar_url"
            :img-alt="contributor.login"
            img-top
            style="max-width: 20rem;"
            class="mb-2 git-user"
          >
            <b-card-text v-if="contributor.login != 'denBot'">
              Commits: {{ contributor.contributions }}
            </b-card-text>

            <b-card-text v-else>
              Conmmits: Over 9,000!!!
            </b-card-text>

          </b-card>
        </a>
    </b-col-md-2>
    <b-col-md-3></b-col-md-3>
    </b-row>

    <br/><br/>
    
    <div class="info-deps">
    <div v-if="myGitHubData.repository">
      <h1>Project Information</h1>
      <ul>
        <li>Name: {{ myGitHubData.repository.name }}</li>
        <li>Owner: {{ myGitHubData.repository.owner.login }}</li>
        <li>Created: {{ myGitHubData.repository.created_at }}</li>
        <li>Last updated: {{ myGitHubData.repository.updated_at }}</li>
        <li>Project URL: <a :href="myGitHubData.repository.html_url">{{  myGitHubData.repository.html_url }}</a></li>
      </ul>
    </div>
      <br/>
      <h1>Django Dependencies </h1>
      
      <ul>
        <li :key="dep" v-for="dep in djangoDependencies"><a :href="dep.url">{{ dep.title }}</a></li>
      </ul>
      <br/>
      <h1>Vue Dependencies</h1>
      <ul>
        <li :key="dep" v-for="dep in vueDependencies"><a :href="dep.url">{{ dep.title }}</a></li>
      </ul>
    </div>
    </div>
  </div>

    
    

  </div>
</template>
<!--
    vue-router
    vue-video-player
    vuex
    wavesurfer.js
  },
  -->

<script>
    export default {
      name: "About",
      data () {
          return {
            myGitHubData: {},

            djangoDependencies: 
              [
                {
                  "title": "Django 1.11.18",
                  "url": "https://docs.djangoproject.com/en/2.1/releases/1.11.18/"
                },
                {
                  "title": "Django Rest Framework",
                  "url": "https://www.django-rest-framework.org/"
                },
                {
                  "title": "Django REST Framework - simplejwt",
                  "url": "https://github.com/davesque/django-rest-framework-simplejwt"
                },
                {
                  "title": "Django Cors Headers",
                  "url": "https://github.com/ottoyiu/django-cors-headers"
                },
                {
                  "title": "Django Model Admin Reorder",
                  "url": "https://pypi.org/project/django-modeladmin-reorder/"
                },
                {
                  "title": "Django Webpack Loader",
                  "url": "https://github.com/owais/django-webpack-loader"
                },

                {
                  "title": "Easy Thumbnails",
                  "url": "https://github.com/SmileyChris/easy-thumbnails"
                },
                {
                  "title": "Easy Thumbnails FFMPEG",
                  "url": "https://github.com/denBot/easy-thumbnails-ffmpeg"
                },
                {
                  "title": "hurry.filesize",
                  "url": "https://pypi.org/project/hurry.filesize/"
                },
                {
                  "title": "MailChecker",
                  "url": "https://pypi.org/project/mailchecker/"
                },
                {
                  "title": "MoviePy",
                  "url": "https://zulko.github.io/moviepy/"
                },
                {
                  "title": "Pillow",
                  "url": "https://pillow.readthedocs.io/en/stable/"
                },
                {
                  "title": "virustotal-api",
                  "url": "https://pypi.org/project/virustotal-api/"
                }



              ],
              vueDependencies: [
                {
                  "title": "VueJS",
                  "url": "https://vuejs.org/"
                },
                {
                  "title": "Vue FontAwesome",
                  "url": "https://github.com/FortAwesome/vue-fontawesome"
                },
                                {
                  "title": "Axios",
                  "url": "https://github.com/axios/axios"
                },
                {
                  "title": "Bootstrap Vue",
                  "url": "https://bootstrap-vue.js.org/"
                },
                {
                  "title": "highlight.js",
                  "url": "https://highlightjs.org/"
                },
                {
                  "title": "jwt-decode",
                  "url": "https://www.npmjs.com/package/jwt-decode"
                },
                {
                  "title": "Video.js",
                  "url": "https://videojs.com/"
                },
                {
                  "title": "VueJS",
                  "url": "https://vuejs.org/"
                },
                {
                  "title": "vue-color",
                  "url": "https://github.com/xiaokaike/vue-color"
                },
                {
                  "title": "vue-github-api",
                  "url": "https://www.npmjs.com/package/vue-github-api"
                },
                {
                  "title": "vue-notification",
                  "url": "https://www.npmjs.com/package/vue-notification"
                },
                {
                  "title": "vue-paginate",
                  "url": "https://github.com/TahaSh/vue-paginate"
                },
                {
                  "title": "vue-router",
                  "url": "https://router.vuejs.org/"
                },
                {
                  "title": "vue-video-player",
                  "url": "https://github.com/surmon-china/vue-video-player"
                },
                {
                  "title": "vuex",
                  "url": "https://vuex.vuejs.org/"
                },
                {
                  "title": "vue-password-strength-meter",
                  "url": "https://github.com/apertureless/vue-password-strength-meter"
                },
                {
                  "title": "wavesurfer.js",
                  "url": "https://wavesurfer-js.org/"
                },

              ]
            }
          },
        created() {
          this.GitHubAPI.get('/repos/denBot/WAD2-Group-Project/contributors', {}, [this.myGitHubData, 'contributors'])
          this.GitHubAPI.get('/repos/denBot/WAD2-Group-Project', {}, [this.myGitHubData, 'repository'])
        },
        mounted() {
          console.log(this.myGitHubData);
        }
    }
</script>

<style scoped>
a {
  color: 
}
.info-deps {
  padding: 20px;
}
.about-container {
  background-color: rgba(0,0,0,0.2);
  padding: 50px;
}
.git-user {
  max-width: 17rem !important;
  margin: 0px 10px;
}

.git-user img {
  width: 220px;
}
.card-title, .card-text {
  color: #242424;
}
.git-href, .git-href:visited, .git-href:active, .git-href:hover {
  color: transparent;
}
.project-information {
    margin: 0;
    background-color: #191919;
    padding: 30px;
    border: 1px solid black;
}
.contributor-header {
  text-align: center;
  padding: 10px;
}

</style>
