// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'

// axios
import axios from 'axios'
import VueAxios from 'vue-axios'
Vue.use(VueAxios, axios)

// bootstrap
import BootsrtapVue from 'bootstrap-vue'
Vue.use(BootsrtapVue)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// import test data
import krizanke from '../test_data/krizanke100.json'
var testInitList = []
for (var i=0; i<krizanke["one"].length; i++) {
  testInitList.push({"filename": krizanke["one"][i], "number": i})
}

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  components: { App },
  template: '<App/>',
  data () { return {
    // apiAddress: "http://127.0.0.1:5001",
    apiAddress: "http://192.168.2.1:5001",
    errMsg: "",
    initList: testInitList,
  }},
})
