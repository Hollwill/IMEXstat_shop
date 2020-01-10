import Vue from 'vue'
import App from './App.vue'

import VueRouter from 'vue-router'

Vue.use(VueRouter);

Vue.prototype.$eventHub = new Vue();

var router = new VueRouter({
  routes: [
    {path: '/market_summary', name: 'market_summary', props: true, component: () => import('./BaseMarketSummary.vue')},
    {path: '/report_tnved', name: 'report_tnved', props: true, component: () => import('./ReportByTnved.vue')},
    {path: '/report_country', name: 'report_country', props: true, component: () => import('./ReportByCountry.vue')},
    {path: '/report_region', name: 'report_region', props: true, component: () => import('./ReportByRegion.vue')},
  ]
});

Vue.config.productionTip = false

new Vue({
  router: router,
  render: h => h(App)
}).$mount('#app');

