import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import VueNativeNotification from 'vue-native-notification'
import VueClipboard from 'vue-clipboard2'
import axios from 'axios'
import VueOverflowScroll from 'vue-overflow-scroll'



VueClipboard.config.autoSetContainer = true // add this line
Vue.use(VueClipboard)
Vue.use(VueOverflowScroll)
Vue.config.productionTip = false
Vue.use(VueNativeNotification, {
  // Automatic permission request before
  // showing notification (default: true)
  requestOnNotify: false
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
