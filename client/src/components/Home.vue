/**
 * Component for the Home page.
 *
 * This component displays a form for deleting and uploading tracks to a Toniebox.
 * It also provides a form for downloading tracks from YouTube.
 *
 * @component
 * @example
 * <Home />
 */
<template v-if='content'>
  <main role="main">
    <!-- Tonies component -->
    <Tonies :tonies="creativetonies" @onchange="getContent($event)" />
    <div class="container">
      <div class="row">
        <div class="col">
          <!-- Delete form  s-->
          <form @submit="onSubmit" method="post" v-if="content">
            <span v-if="chapters.length">Minutes Remaining on Tonie:
              {{ Math.floor(content.tracks.secondsRemaining / 60) }}</span>
            <div v-if="chapters.length">Total Runtime: {{ formatTime(totalRuntime) }}</div>
            <div v-for="track in chapters" :key="track.id" class="col-md-11">
              <label class="list-group-item gap-3">
                <input class="form-check-input" type="checkbox" v-bind:value="track.id" style="font-size: 0.375em;"
                  v-model="deleteFromTonie">
                <span class="form-checked-content">
                  <div v-if="track.title.length < 20">
                    <strong>{{ track.title }}</strong>
                  </div>
                  <div v-else>
                    <strong>{{ track.title.substring(0, 20) }}...</strong>
                  </div>
                  <small class="text-muted">
                    <svg class="bi me-1" width="1em" height="1em">
                      <use xlink:href="#calendar-event"></use>
                    </svg>
                    
                    {{ `${Math.floor((track.seconds % 3600) / 60)
                      .toString()
                      .padStart(2, '0')}:${Math.floor(track.seconds % 60).toString().padStart(2, '0')}` }}
                  </small>
                </span>
              </label>
            </div>
            <button type="submit" class="btn btn-danger">Delete Selected Files</button>
          </form>
        </div>
        <div class="col">
          <!-- Download form -->
          <form @submit="downloadYoutube" method="post">
            <div class="input-group mb-3">
              <input type="text" class="form-control" placeholder="Youtube URL" aria-label="Youtube URL"
                aria-describedby="button-addon2" v-model="youtubeUrl">
              <button class="btn btn-outline-secondary" type="submit" id="button-addon2">Download</button>
            </div>
          </form>
          <!-- Upload form -->
          <form @submit="onSubmitUpload" method="post" v-if="content">
            <div v-for="song in songs" :key="song.file" class="col-md-11">
              <label class="list-group-item gap-3">
                <input class="form-check-input" type="checkbox" v-bind:value="song.file" style="font-size: 0.375em;"
                  v-model='uploadToTonie'>
                <span class="form-checked-content">
                  <strong>{{ song.file }}</strong>
                </span>
              </label>
            </div>
            <button type="submit" class="btn btn-success">Upload Selected Files</button>
            <button type="button" class="btn btn-primary" @click="Refresh">Refresh</button>
            <button type="button" class="btn btn-danger" @click="deleteLocalTrack">Delete Local Tracks</button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
<script>
/**
 * @file Home.vue
 * @description This file contains the implementation of the Home component.
 * The Home component is responsible for displaying the home page of the application.
 * It fetches data from the backend server and provides methods for interacting with the server.
 */

import axios from 'axios';
import Tonies from './Tonies.vue';

const backendUrl = `${process.env.VUE_APP_BACKEND_SCHEME}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`;

/**
 * Compare function for sorting strings or numbers in ascending order.
 * @param {string|number} a - The first value to compare.
 * @param {string|number} b - The second value to compare.
 * @returns {number} - Returns -1 if a < b, 1 if a > b, and 0 if a = b.
 */
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
    /**
     * Compare function for sorting songs based on their file names.
     * @param {object} lhs - The first song object to compare.
     * @param {object} rhs - The second song object to compare.
     * @returns {number} - Returns -1 if lhs.file < rhs.file, 1 if lhs.file > rhs.file, and 0 if lhs.file = rhs.file.
     */
    cmpSongs(lhs, rhs) {
      return cmp(lhs.file, rhs.file);
    },
    /**
     * Fetches the content of a creative tonie from the backend server.
     * @param {string} creativeTonie - The ID of the creative tonie.
     * @param {string} audiobookID - The ID of the audiobook.
     */
    getContent(creativeTonie, audiobookID) {
      const path = `${backendUrl}/tonie_overview`;
      this.selectedTonie = creativeTonie;
      console.log(audiobookID);
      console.log('creativeTonie', creativeTonie);
      axios.post(path, { tonie_id: creativeTonie })
        .then((res) => {
          this.chapters = res.data.tracks.chapters;
          this.content = res.data;
          console.log(this.content);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    /**
     * Fetches the list of creative tonies from the backend server.
     */
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
    /**
     * Fetches the list of audio tracks on the disk from the backend server.
     */
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
    /**
     * Deletes a local track from the disk.
     */
    deleteLocalTrack() {
      console.log('deleteLocalTrack', this.uploadToTonie);
      const path = `${backendUrl}/delete_local_track`;
      axios.post(path, { file: this.uploadToTonie })
        .then((res) => {
          console.log(res);
          this.getAudioOnDisk();
          this.uploadToTonie = [];
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    /**
     * Deletes a track from a creative tonie.
     * @param {Event} e - The submit event.
     */
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
    /**
     * Uploads a track to a creative tonie.
     * @param {Event} e - The submit event.
     */
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
    /**
     * Downloads audio from a YouTube URL.
     * @param {Event} e - The submit event.
     */
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
    /**
     * Formats a time in seconds to a string in the format "HH:MM:SS".
     * @param {number} seconds - The time in seconds.
     * @returns {string} - The time in the format "HH:MM:SS".
     */
    formatTime(seconds) {
      const hrs = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);
      return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    /**
     * Refreshes the data on the page by fetching the latest data from the backend server.
     */
    Refresh() {
      this.getAudioOnDisk();
      this.getCreativeTonies();
    },
  },
  computed: {
    /**
     * Computes the total runtime of the selected tracks.
     * @returns {number} - The total runtime of the selected tracks in seconds.
     */
    totalRuntime() {
      return this.chapters.reduce((total, track) => total + track.seconds, 0);
    },
  },
  created() {
    this.getCreativeTonies();
    this.getAudioOnDisk();
  },
};
</script>
