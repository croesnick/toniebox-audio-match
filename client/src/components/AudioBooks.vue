<template>
  <main role="main">
    <div class="album py-5 bg-light">
      <div class="container">
        <div class="row">
          <div v-for="audiobook in audiobooks" :key="audiobook.id" class="col-md-3">
            <div class="card mb-4 shadow-sm">
              <div v-if="audiobook.cover_uri !== null">
                <img :src="'./assets/covers/' + audiobook.cover_uri"
                     class="card-img-top"
                     :alt="audiobook.title">
              </div>
              <div v-else>
                <svg class="bd-placeholder-img card-img-top" width="100%" height="253"
                     xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice"
                     focusable="false" role="img" aria-label="Placeholder: Thumbnail">
                  <title>no cover</title>
                  <rect width="100%" height="100%" fill="#55595c"/>
                  <text x="50%" y="50%" fill="#eceeef" dy=".3em">no cover</text>
                </svg>
              </div>
              <div class="card-body">
                <h5 class="card-title">{{ audiobook.title }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ audiobook.artist }}</h6>
              </div>
              <Tonies :tonies="creativetonies"
                      :audiobookID="audiobook.id"
                      @onchange="uploadAlbumToTonie"/>
            </div>
            <!--            <div class="d-flex justify-content-between align-items-center">-->
            <!--              <small class="text-muted">35 mins</small>-->
            <!--            </div>-->
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import Tonies from './Tonies.vue';

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';

export default {
  components: { Tonies },
  data() {
    return {
      audiobooks: [],
      creativetonies: [],
    };
  },
  methods: {
    getAudiobooks() {
      const path = 'http://localhost:8080/audiobooks';
      axios.get(path)
        .then((res) => {
          this.audiobooks = res.data.audiobooks;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getCreativeTonies() {
      const path = 'http://localhost:8080/creativetonies';
      axios.get(path)
        .then((res) => {
          this.creativetonies = res.data.creativetonies;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    uploadAlbumToTonie(tonieID, audiobookID) {
      const path = 'http://localhost:8080/upload';
      axios.post(path, { tonie_id: tonieID, audiobook_id: audiobookID })
        .then((res) => {
          // eslint-disable-next-line
          console.log('Upload id: ' + res.data.upload_id);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getAudiobooks();
    this.getCreativeTonies();
  },
};
</script>
