<template v-if='content'>
  <main role="main">
    <Tonies :tonies="creativetonies" @onchange="getContent"/>
      <div class="container">
        <div class="row">
          <div class="col">
              <form @submit="onSubmit" method="post" v-if="content">
                <div v-for="track in chapters" :key="track.id" class="col-md-3">
                  <label class="list-group-item d-flex gap-3">
                    <input class="form-check-input" type="checkbox"
                        v-bind:value="track.id" style="font-size: 1.375em;"
                        v-model='deleteFromTonie' checked>
                    <span class="pt-1 form-checked-content">
                      <strong>{{track.title}}</strong>
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
            <form @submit="onSubmitUpload" method="post" v-if="content">
              <div v-for="song in songs" :key="song.id" class="col-md-3">
                <label class="list-group-item d-flex gap-3">
                  <input class="form-check-input" type="checkbox"
                    v-bind:value="song.id" style="font-size: 1.375em;"
                    v-model='uploadToTonie' checked>
                  <span class="pt-1 form-checked-content">
                    <strong>{{song.title}}</strong>
                  </span>
                </label>
              </div>
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
      songs: [],
    };
  },
  cmp,
  methods: {
    cmpSongs(lhs, rhs) {
      return cmp(lhs.file, rhs.file);
    },
    getContent(creativeTonie, audiobookID) {
      const path = `${backendUrl}/tonie_overview`;
      console.log(creativeTonie);
      console.log(audiobookID);
      axios.post(path, { tonie_id: creativeTonie })
        .then((res) => {
          this.content = res.data;
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
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onSubmit(e) {
      e.preventDefault();
      const path = `${backendUrl}/delete_track`;
      console.log(path);
      console.log('DeleteFromTonie', this.deleteFromTonie);
      axios.post(path, { tonie_id: 'EDE61A15500304E0', track_id: this.deleteFromTonie })
        .then((res) => {
          console.log('res', res);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getContent();
    this.getCreativeTonies();
  },
};
</script>
