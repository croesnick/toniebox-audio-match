<template>
  <main role="main">
    <div class="album py-5 bg-light">
      <div class="container">
        <div class="row">
          <div v-for="song in songs" :key="song.file" class="col-md-3">
            <div class="card mb-4 shadow-sm">
              <div>
                <!-- Placeholder image for the song -->
                <svg class="bd-placeholder-img card-img-top" width="100%" height="253"
                     xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice"
                     focusable="false" role="img" aria-label="Placeholder: Thumbnail">
                  <title>no cover</title>
                  <rect width="100%" height="100%" fill="#55595c"/>
                  <text x="50%" y="50%" fill="#eceeef" dy=".3em">no cover</text>
                </svg>
              </div>
              <div class="card-body">
                <h5 class="card-title">
                  <!-- Display the song file name -->
                  {{ song.file}}
                  <div v-if="song.disc !== null"> ({{ song.disc }})</div>
                </h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ song.file}}</h6>
              </div>
              <!-- Tonies component to handle tonie selection -->
              <Tonies :tonies="creativetonies"
                      :audiobookID="song.id"
                      @onchange="uploadAlbumToTonie"/>
            </div>
            <!-- Additional card content -->
            <!-- <div class="d-flex justify-content-between align-items-center">
              <small class="text-muted">35 mins</small>
            </div> -->
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import Tonies from './Tonies.vue';

// Backend URL based on environment variables
const backendUrl = `${process.env.VUE_APP_BACKEND_SCHEME}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`;

console.log('backendUrl', backendUrl);

// Comparison function for sorting songs
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
      songs: [], // Array to store songs
      creativetonies: [], // Array to store creative tonies
    };
  },
  cmp, // Comparison function for sorting songs
  methods: {
    // Comparison function for sorting songs by file name
    cmpSongs(lhs, rhs) {
      return cmp(lhs.file, rhs.file);
    },
    // Fetch songs from the backend API
    getSongs() {
      const path = `${backendUrl}/songs`;
      axios.get(path)
        .then((res) => {
          this.songs = res.data.songs.sort(this.cmpSongs);
        })
        .catch((error) => {
          // Handle error
          console.error(error);
        });
    },
    // Fetch creative tonies from the backend API
    getCreativeTonies() {
      const path = `${backendUrl}/creativetonies`;
      axios.get(path)
        .then((res) => {
          this.creativetonies = res.data.creativetonies;
        })
        .catch((error) => {
          // Handle error
          console.error(error);
        });
    },
    // Upload album to selected tonie
    uploadAlbumToTonie(tonieID, audiobookID) {
      const path = `${backendUrl}/upload`;
      axios.post(path, { tonie_id: tonieID, audiobook_id: audiobookID })
        .then((res) => {
          // Log the upload ID
          console.log('Upload id: ' + res.data.upload_id);
        })
        .catch((error) => {
          // Handle error
          console.error(error);
        });
    },
  },
  created() {
    // Fetch songs and creative tonies when the component is created
    this.getSongs();
    this.getCreativeTonies();
  },
};
</script>
