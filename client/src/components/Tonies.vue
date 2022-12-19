<template>
  <select class="form-control" @change="tonieSelected">
    <option selected disabled>Wähle deinen Tonie</option>
    <option v-for="tonie in tonies" :key="tonie.id" :value="tonie.id">
      {{ tonie.name }}
    </option>
  </select>
</template>

<script>
export default {
  props: {
    tonies: [Array],
    audiobookID: String,
  },
  methods: {
    tonieSelected(event) {
      // eslint-disable-next-line
      this.$emit('onchange', event.target.value, this.audiobookID);
    },
  },
};
</script>
