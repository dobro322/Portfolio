import Vue from 'vue'
import Router from 'vue-router'
import Main from './views/Main.vue'
import Reservation from './views/Reservation.vue'
import Logging from './views/Logging.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/Logging',
      name: 'Loggin',
      component: Logging
    },
    {
      path: '/reservation',
      name: 'Reservation',
      component: Reservation
    },
  ]
})
