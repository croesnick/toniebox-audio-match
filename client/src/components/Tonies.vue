<template>
  <select class="form-control" @change="tonieSelected">
    <option disabled value="">Wähle deinen Tonie</option>
    <option v-for="tonie in tonies" :key="tonie.id" :value="tonie.id">
      {{ tonie.name }}
    </option>
  </select>
</template>

<script>
export default {
  props: {
    tonies: String,
    audiobookID: String,
  },
  methods: {
    tonieSelected(event) {
      // eslint-disable-next-line
      alert('Starting upload. Your tonie will be ready in a few minutes! :)');
      this.$emit('onchange', event.target.value, this.audiobookID);
    },
  },
};
</script>
