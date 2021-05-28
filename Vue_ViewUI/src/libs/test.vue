<template>

</template>

<script>
import Vue from "vue";

export default {
  name: "test",
  methods: {
    /**
     * 向 Vuex 注册空调
     * @param acInfo
     */
    addAC: function (acInfo) {
      Vue.set(this.$store.state.roomInfo, acInfo.rid, acInfo);
      console.log(this.$store.state);
      return true;
    },
  }
}
</script>

<style scoped>

</style>