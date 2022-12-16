import Vue from 'vue';
import Router from 'vue-router';
import AudioBooks from './components/AudioBooks.vue';
import Songs from './components/Songs.vue';

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
    {
      path: '/songs',
      name: 'Songs',
      component: Songs,
    },
  ],
});
