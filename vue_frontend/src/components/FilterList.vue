<template>
  <div class="container">
    <div v-if="$root.errMsg !== ''" class="row text-warning">
      {{ $root.errMsg }}
    </div>
    <div class="row my-center">
      <ControlButton
          control-state-prop="on"
          v-bind:activated="projectorState.on"
          btn-text="Vklop"/>
      <ControlButton
          control-state-prop="sleep"
          v-bind:activated="projectorState.sleep"
          btn-text="Spanje"/>
    </div>
    <div class="row my-min-height my-center">
      <!--div class="col-xs-6">
        <p>Predvaja se:&nbsp;&nbsp;&nbsp;&nbsp;</p>
      </div-->
      <Loader v-if="loading"></Loader>
      <p v-else>{{ selected }}</p>
    </div>
    <div class="row pb-2">
      <input class="form-control" v-model="filter" type="text" placeholder="iskanje">
    </div>
    <div class="row">
        <table class="table table-bordered">
          <tbody>
            <tr
              v-for="(el, idx) in filteredList"
              v-on:click="selectEl(el, idx)"
              v-bind:class="{ 'table-info': idx === selectedIdx }"
            >
              <td>{{ el }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>
</template>

<script>
import Loader from "./Loader.vue"
import ControlButton from "./ControlButton.vue"

export default {
  name: "FilterList",
  components: {
    Loader,
    ControlButton,
  },
  data () { return {
    projectorState: {
      on: false,
      sleep: false,
    },
    loading: false,
    selected: "",
    selectedIdx: -1,
    filter: "",
    prevFilter: "",
    list: ["Song number 1", "2. song", "3_some_title", "fourth song"],
    filteredList: [],
  }},
  created: function () {
    this.list = this.$root.krizanke["one"]
    this.updateList()
  },
  watch: {
    filter: function () {
      this.updateList()
      this.selectedIndex = -1
    },
  },
  methods: {
    isSelected: function (el) {
      return (el === this.selected)
    },
    selectEl: function (el, idx) {
      var testErr = false// dev

      this.selectedIdx = idx
      this.loading = true
      this.$root.errMsg = ""
      var tmpThis = this
      this.axios.get("http://jsonplaceholder.typicode.com/posts")
        .then(response => {
          var mockResponse = {
            selected: el,
          }
          // todo reponse should be same as sent el (confirmation from server)
          // else, error
          if (testErr) {
            tmpThis.$root.errMsg= "Error: mismatching request and response."
          }
          tmpThis.selected = mockResponse.selected
          tmpThis.loading = false
        })
        .catch(err => {
          tmpThis.loading = false
          tmpThis.$root.errMsg= err.message
        })
    },
    updateList: function () {
      var inList = []
      if (this.filter.length <= this.prevFilter.length) {
        inList = this.list
      } else {
        inList = this.filteredList
      }

      var filter = this.filter.toLowerCase()
      var outList = []
      inList.forEach(function(el) {
        if (el.toLowerCase().indexOf(filter) !== -1) {
          outList.push(el)
        }
      })

      this.prevFilter = this.filter
      this.filteredList = outList
    },
    mySleep: function (nsec, callback) {
      console.log("Sleeping for " + nsec + "sec.")
      var start = new Date().getTime();
      for (var i = 0; i < 1e7; i++) {
        if ((new Date().getTime() - start) > nsec * 1000){
          break;
        }
      }
      callback()
    },
    controlCommand: function (cmd) {
      console.log("received from child: " + cmd)
      this.projectorState[cmd] = !this.projectorState[cmd]
    }
  },
}
</script>

<style>
  .my-center * {
    margin: auto;
  }
  .my-min-height {
    min-height: 50px;
  }
</style>
