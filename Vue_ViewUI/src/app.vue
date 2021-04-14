<style scoped>
@import 'styles/common.css';


</style>
<template>
  <div>
    <router-view></router-view>
    <p class="Footer">
      by Ridd.
    </p>
  </div>

</template>
<script>
import admin from './views/adminView/admin.vue';
import clientLogin from "./views/clientView/clientLogin";
import client from "./views/clientView/client";

export default {
  data() {
    return {}
  },
  components: {
    'admin': admin,
    'clientLogin': clientLogin,
    'client': client
  },
  mounted() {

  },
  beforeDestroy() {

  },
  methods: {}
}
</script>
