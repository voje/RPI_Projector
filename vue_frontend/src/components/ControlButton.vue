<template>
  <button v-on:click="controlCommand()" type="button" class="btn btn-wide" v-bind:class="{
    'btn-secondary': !stateOn,
    'btn-primary': stateOn,
    }">{{ btnText }}
  </button>
</template>

<script>
export default {
  name: "ControlButton",
  props: {
    pState: {type: Object},
    stateProp: {type: String},
    btnText: {type: String},
  },
  computed: {
    stateOn: function () {
      return this.pState[this.stateProp]
    }
  },
  methods: {
    controlCommand: function () {
      this.$parent.changeProjectorState(this.stateProp)
    },
  }
}
</script>

<style>
.btn-wide {
  min-width: 40vw;
}
</style>
