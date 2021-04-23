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
import adminLogin from "./views/adminView/adminLogin";
import adminMain from "./views/adminView/adminMain";
import adminSearch from "./views/adminView/adminSearch";
import adminSettings from "./views/adminView/adminSettings";

export default {
  data() {
    return {}
  },
  components: {
    'admin': admin,
    'adminLogin': adminLogin,
    'adminMain': adminMain,
    'adminSearch': adminSearch,
    'adminSettings': adminSettings,
    'clientLogin': clientLogin,
    'client': client,

  },
  mounted() {

  },
  beforeDestroy() {

  },
  methods: {}
}
</script>
