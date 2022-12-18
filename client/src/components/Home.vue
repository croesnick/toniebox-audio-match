<template v-if='content'>
  <main role="main">
  <div class="container-fluid">
    <div class="list-group w-auto col-lg-8 mx-auto">
      <form @submit="onSubmit" method="post">
      <div v-for="track in chapters" :key="track.id" class="col-md-3">
      <label class="list-group-item d-flex gap-3">
        <input class="form-check-input" type="checkbox"
        v-bind:value="track.id" style="font-size: 1.375em;" v-model='deleteFromTonie' checked>
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
      <div>
      <button type="submit" class="btn btn-danger" >
      Delete Selected Files</button>
      </div>
      </form>
    </div>
  </div>
  </main>
</template>
<script>
import axios from 'axios';

const backendUrl = `${process.env.VUE_APP_BACKEND_SCHEME}://${process.env.VUE_APP_BACKEND_HOST}:${process.env.VUE_APP_BACKEND_PORT}`;
console.log(backendUrl);

export default {
  data() {
    return {
      content: [],
      chapters: [],
      creativetonies: [],
      deleteFromTonie: [],
    };
  },
  methods: {
    getContent() {
      const path = `${backendUrl}/tonie_overview`;
      console.log(path);
      axios(path, { tonie_id: 'EDE61A15500304E0' })
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
