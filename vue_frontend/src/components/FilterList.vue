<template>
  <div class="container">
    <div v-if="$root.errMsg !== ''" class="row text-warning">
      {{ $root.errMsg }}
    </div>
    <div class="row my-center mt-3">
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
      <p v-else>{{ selected["filename"] }}</p>
    </div>
    <div class="row p-3">
      <form class="form full-width" v-on:submit.prevent="unfocus()">
        <input
          class="form-control"
          v-bind:value="filter"
          v-on:input="updateInput($event.target.value)"
          type="text"
          placeholder="iskanje">
      </form>
    </div>
    <div class="row">
        <table class="table table-bordered">
          <tbody>
            <tr
              v-for="(el, idx) in filteredList"
              v-on:click="selectEl(el, idx)"
              v-bind:class="{ 'table-info': idx === selectedIdx }"
            >
              <td>{{ el["filename"] }}</td>
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
    selected: {filename: "", number: -1},
    selectedIdx: -1,
    filter: "",
    prevFilter: "",
    list: [],
    filteredList: [],
  }},
  created: function () {
    this.fetchInitData()
    this.updateList()
  },
  watch: {
    filter: function () {
      this.updateList()
      this.selectedIndex = -1
    },
  },
  methods: {
    updateInput: function (val) {
      this.filter = val
    },
    unfocus: function () {
      document.activeElement.blur()
    },
    isSelected: function (el) {
      return (el === this.selected)
    },
    selectEl: function (el, idx) {
      this.selectedIdx = idx
      this.loading = true
      this.$root.errMsg = ""
      var tmpThis = this
      this.axios.get(this.$root.apiAddress + "/display-file?number=" + el["number"])
        .then(response => {
          if (el["number"] !== response.data["displayed_number"]) {
            // console.log(el["number"])
            // console.log(response.data["displayed_number"])
            tmpThis.$root.errMsg= "Error: mismatching request and response."
          } else {
            tmpThis.selected = el
            tmpThis.projectorState = {
              on: (response.data["projector_state"] === "on"),
              sleep: response.data["blank"],
            }
          }
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
        if (el["filename"].toLowerCase().indexOf(filter) !== -1) {
          outList.push(el)
        }
      })

      this.prevFilter = this.filter
      this.filteredList = outList
    },
    controlCommand: function (cmd) {
      var key = ""
      if (cmd === "sleep") key = "KEY_R"
      else if (cmd === "on") {
        if (this.projectorState.on) key = "KEY_P"
        else key = "KEY_O"
      }
      var tmpThis = this
      this.axios.get(this.$root.apiAddress + "/command?key=" + key)
      .then(response => {
        tmpThis.projectorState = {
          on: (response.data["projector_state"] === "on"),
          sleep: response.data["blank"],
        }
      })
      .catch(err => {
        tmpThis.$root.errMsg = err.message
      })
    },
    fetchInitData: function () {
      this.loading = true
      var tmpThis = this
      this.axios.get(this.$root.apiAddress + "/get-files")
      .then(response => {
        tmpThis.list = response.data["files_list"]
        tmpThis.updateList()
        tmpThis.projectorState = {
          on: (response.data["projector_state"] === "on"),
          sleep: response.data["blank"],
        }
        tmpThis.loading = false
      })
      .catch(err => {
        tmpThis.$root.errMsg= err.message + " - Using test list."
        tmpThis.list = tmpThis.$root.initList
        tmpThis.updateList()
        tmpThis.loading = false
      })
    }
  },
}
</script>

<style>
  .full-width {
    width: 100%
  }
  .my-center * {
    margin: auto;
  }
  .my-min-height {
    min-height: 50px;
  }
</style>
