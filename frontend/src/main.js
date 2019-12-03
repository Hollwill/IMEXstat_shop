import Vue from 'vue'
import App from './App.vue'
export const eventBus = new Vue()


Vue.config.productionTip = false

new Vue({
  render: h => h(App)
}).$mount('#app')

//TODO: https://www.highcharts.com/blog/tutorials/highcharts-vue-wrapper/?__cf_chl_jschl_tk__=efedd196a5ca117ee2f5d54ff77f15f483fb1122-1575181514-0-Aa7vCL3WxQsS9sIztBgbRDxB_CDPRWPsAxa3SGeEhpTnnIiPJKA7m5G4otj-Xpgog2AORRBR7RBZLcEymSvyarFvasUwUzqXyVB9svF57rktjNZA97RhacDmXBsKYfCu81rmFfNvYddaQ4sGnIY21vMoHmgT8Cv-4X8YiCNMqwazrfWnSR6UkfdKwrVkehd2oYhSlLI0KC9SEKZTHHnn1VVbGuvDkAZotJ6d69WlyZaCdAlpCmaiJWFvnkF8jbs6zcbLZGwaoyUrUmz0GqA39oCQGIVxGk3q-dZ0Cmmf2ThCJefVjN5LZ3gzVhx_FGHCka6VpI95wZCNHU0nfGwLjhLePBKAnRAz7VMFe8zdhfE3YqebmQCxRWIRcEyZV86CBA