<template>
  <main role="main">
    <div class="list-group w-auto">
      <div v-for="track in content.tracks.chapters" :key="track.id" class="col-md-3">
      <label class="list-group-item d-flex gap-3">
        <input class="form-check-input flex-shrink-0" type="checkbox"
        value checked style="font-size: 1.375em;">
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
    </div>
  </main>
</template>
<script>
import axios from 'axios';

const backendUrl = `${process.env.VUE_APP_BACKEND_SCHEME}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`;

console.log('backendUrl', backendUrl);

export default {
  data() {
    return {
      content: [],
      creativetonies: [],
    };
  },
  methods: {
    getContent() {
      const path = `${backendUrl}/tonie_overview`;
      axios.post(path, { tonie_id: 'EDE61A15500304E0' })
        .then((res) => {
          this.content = res.data;
          console.log('content', this.content);
          console.log('tracks', this.content.tracks.chapters);
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
  },
  created() {
    this.getContent();
    this.getCreativeTonies();
  },
};
</script>
