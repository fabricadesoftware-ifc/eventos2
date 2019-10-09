import Vue from 'vue';
import Router from 'vue-router';

import i18n from './i18n';

import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/:lang',
      component: {
        template: '<router-view></router-view>',
      },
      beforeEnter(to, from, next) {
        const { lang } = to.params;
        if (!['pt', 'en'].includes(lang)) {
          return next('en');
        }
        i18n.locale = lang;
        return next();
      },
      children: [
        {
          path: '/',
          name: 'home',
          component: Home,
        },
        // {
        //   path: '/about',
        //   name: 'about',
        //   // route level code-splitting
        //   // this generates a separate chunk (about.[hash].js) for this route
        //   // which is lazy-loaded when the route is visited.
        //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
        // },
      ],
    },
  ],
});
