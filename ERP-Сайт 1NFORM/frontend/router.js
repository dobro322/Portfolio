import Vue from 'vue'
import Router from 'vue-router'
import Quests from './views/Quests.vue'
import Surfers from './views/Surfers.vue'
import Fundraising from './views/Fundraising.vue'
import Filtration from './views/Filtration.vue'
import Companions from './views/Companions.vue'
import Kanban from './views/Kanban.vue'
import Kanbanviewer from './views/Kanbanviewer.vue'
import User from './views/User.vue'
import Moderate from './views/Admin.vue'
import Main from './views/Main.vue'
import TeamCard from './components/TeamCard.vue'
import Rating from './components/Rating.vue'
import Additional from './views/Additional.vue'
import Logging from './views/Logging.vue'
import Tickets from './views/Tickets.vue'
import Event from './views/Event.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/Quests',
      name: 'Quests',
      component: Quests
    },
    {
      path: '/',
      name: 'Main',
      component: Main
    },
    {
      path: '/Moderate',
      name: 'Moderate',
      component: Moderate
    },
    {
      path: '/Tickets',
      name: 'Tickets',
      component: Tickets
    },
    {
      path: '/Surfers',
      name: 'Surfers',
      component: Surfers
    },
    {
      path: '/Additional',
      name: 'Additional',
      component: Additional,
      children: [
        { path: 'Filtration', component: Filtration},
        { path: 'Fundraising', component: Fundraising},
      ]
    },
    {
      path: '/Companions',
      name: 'Companions',
      component: Companions,
      children: [
        { path: '/Companions/Team', component: TeamCard},
        { path: '/Companions/Rating', component: Rating},
      ]
    },
    {
      path: '/Kanbanviewer',
      name: 'Kanbanviewer',
      component: Kanbanviewer,
      children: [
        { path: '/Kanbanviewer/:dep', component: Kanban },
      ]
    },
    {
      path: '/Companions/Team/:id',
      name: 'User',
      component: User
    },
    {
      path: '/Logging',
      name: 'Loggin',
      component: Logging
    },
    {
      path: '/Event',
      name: 'Event',
      component: Event
    }
  ]
})
