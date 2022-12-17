import Vue from 'vue';
import Router from 'vue-router';
import AudioBooks from './components/AudioBooks.vue';
import Songs from './components/Songs.vue';
import Home from './components/Home.vue';

Vue.use(Router);
export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/audiobooks',
      name: 'AudioBooks',
      component: AudioBooks,
    },
    {
      path: '/songs',
      name: 'Songs',
      component: Songs,
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
  ],
});
