<style scoped>
@import 'styles/common.css';


</style>
<template>
  <div>
    <router-view></router-view>
    <p class="Footer">Designed by Ridd.</p>
  </div>

</template>
<script>
import admin from './views/adminView/admin.vue';
import clientLogin from "./views/clientView/clientLogin.vue";
import client from "./views/clientView/client.vue";
import netInterfaceTest from "./views/netInterfaceTest";
import welcome from "./views/welcome";
import connect_token from "./connect_token"
import Vue from "vue";

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
