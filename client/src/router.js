import Vue from 'vue';
import Router from 'vue-router';
import AudioBooks from './components/AudioBooks.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'AudioBooks',
      component: AudioBooks,
    },
  ],
});
