<template>
  <button v-on:click="controlCommand()" type="button" class="btn btn-wide" v-bind:class="{
    'btn-secondary': !activated,
    'btn-primary': activated,
    }">{{ btnText }}
  </button>
</template>

<script>
export default {
  name: "ControlButton",
  props: {
    activated: {type: Boolean},
    btnText: {type: String},
    controlStateProp: {type: String},
  },
  methods: {
    controlCommand: function () {
      console.log("sending control command to parent: " + this.controlStateProp)
      this.$parent.controlCommand(this.controlStateProp)
    },
  }
}
</script>

<style>
.btn-wide {
  min-width: 40vw;
}
</style>
