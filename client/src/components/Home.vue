<template v-if='content'>
  <main role="main">
    <Tonies :tonies="creativetonies" @onchange="getContent($event)"/>
      <div class="container">
        <div class="row">
          <div class="col">
              <form @submit="onSubmit" method="post" v-if="content">
                <div v-for="track in chapters" :key="track.id" class="col-md-11">
                  <label class="list-group-item gap-3">
                    <input class="form-check-input" type="checkbox"
                        v-bind:value="track.id" style="font-size: 0.375em;"
                        v-model="deleteFromTonie">
                    <span class="form-checked-content">
                      <div v-if="track.title.length<20">
                        <strong>{{track.title}}</strong>
                      </div>
                      <div v-else>
                        <strong>{{track.title.substring(0,20)}}...</strong>
                      </div>
                      <small class="text-muted">
                        <svg class="bi me-1" width="1em" height="1em">
                          <use xlink:href="#calendar-event"></use>
                        </svg>
                           {{Math.floor(track.seconds/60)}}:{{parseInt(track.seconds%60)}}
                      </small>
                    </span>
                  </label>
                </div>
                  <button type="submit" class="btn btn-danger" >
                  Delete Selected Files</button>
              </form>
            </div>
          <div class="col">
            <form @submit="downloadYoutube" method="post">
              <div class="input-group mb-3">
                <input type="text" class="form-control" placeholder="Youtube URL"
                  aria-label="Youtube URL" aria-describedby="button-addon2"
                  v-model="youtubeUrl">
                <button class="btn btn-outline-secondary" type="submit"
                  id="button-addon2">Download</button>
              </div>
            </form>
            <form @submit="onSubmitUpload" method="post" v-if="content">
              <div v-for="song in songs" :key="song.file" class="col-md-11">
                <label class="list-group-item gap-3">
                  <input class="form-check-input" type="checkbox"
                    v-bind:value="song.file" style="font-size: 0.375em;"
                    v-model='uploadToTonie' >
                  <span class="form-checked-content">
                    <strong>{{song.file}}</strong>
                  </span>
                </label>
              </div>
                <button type="submit" class="btn btn-success" >Upload Selected Files</button>
                <button type="button" class="btn btn-primary" @click="Refresh">Refresh</button>
            </form>
          </div>
      </div>
    </div>
  </main>
</template>
<script>
import axios from 'axios';
import Tonies from './Tonies.vue';

const backendUrl = `${process.env.VUE_APP_BACKEND_SCHEME}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`;

function cmp(a, b) {
  if (!a && !b) {
    return 0;
  }
  if (!a) {
    return 1;
  }
  if (!b) {
    return -1;
  }

  if (typeof a === 'string') {
    return a.localeCompare(b);
  }

  if (a < b) {
    return -1;
  }
  return a > b ? 1 : 0;
}

export default {
  components: { Tonies },
  data() {
    return {
      content: [],
      chapters: [],
      creativetonies: [],
      deleteFromTonie: [],
      uploadToTonie: [],
      songs: [],
      youtubeUrl: '',
      selectedTonie: String,
    };
  },
  cmp,
  methods: {
    cmpSongs(lhs, rhs) {
      return cmp(lhs.file, rhs.file);
    },
    getContent(creativeTonie, audiobookID) {
      const path = `${backendUrl}/tonie_overview`;
      this.selectedTonie = creativeTonie;
      console.log(audiobookID);
      console.log('creativeTonie', creativeTonie);
      axios.post(path, { tonie_id: creativeTonie })
        .then((res) => {
          this.chapters = res.data.tracks.chapters;
          console.log(this.content);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getCreativeTonies() {
      const path = `${backendUrl}/creativetonies`;
      axios.get(path)
        .then((res) => {
          this.creativetonies = res.data.creativetonies;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getAudioOnDisk() {
      const path = `${backendUrl}/songs`;
      axios.get(path)
        .then((res) => {
          this.songs = res.data.songs.sort(this.cmpSongs);
          console.log(this.songs);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(e) {
      e.preventDefault();
      const path = `${backendUrl}/delete_track`;
      console.log('DeleteFromTonie', this.deleteFromTonie);
      console.log('Tonie', this.selectedTonie);
      axios.post(path, { tonie_id: this.selectedTonie, track_id: this.deleteFromTonie })
        .then((res) => {
          console.log('res', res);
          this.getContent(this.selectedTonie);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmitUpload(e) {
      e.preventDefault();
      const path = `${backendUrl}/upload_track`;
      console.log('UploadToTonie', this.uploadToTonie);
      console.log('Tonie', this.selectedTonie);
      axios.post(path, { tonie_id: this.selectedTonie, track_ids: this.uploadToTonie })
        .then((res) => {
          // eslint-disable-next-line
          console.log('res', res);
          this.getContent(this.selectedTonie);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    downloadYoutube(e) {
      e.preventDefault();
      const path = `${backendUrl}/download_youtube`;
      console.log('DownloadYoutube', this.youtubeUrl);
      axios.post(path, { youtube_url: this.youtubeUrl })
        .then((res) => {
          // eslint-disable-next-line
          console.log('res', res);
          this.getAudioOnDisk();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    Refresh() {
      this.getAudioOnDisk();
      this.getCreativeTonies();
    },
  },
  created() {
    this.getCreativeTonies();
    this.getAudioOnDisk();
  },
};
</script>
