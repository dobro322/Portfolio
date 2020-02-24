import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import { VueReCaptcha } from 'vue-recaptcha-v3';
Vue.use(VueReCaptcha, { siteKey: '6LdIb60UAAAAAAEEbQYN0DxRfW5HR1UYtP-JKYrY' })
Vue.config.productionTip = false
Vue.options.delimiters = ['[[', ']]'];
Vue.config.delimiters = ['[[', ']]'];

new Vue({
  router,
  render: h => h(App),
  delimiters: ['[[', ']]']
}).$mount('#app')

Vue.options.delimiters = ['[[', ']]'];
Vue.config.delimiters = ['[[', ']]'];
