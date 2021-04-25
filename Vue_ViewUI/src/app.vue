<style src="./assets/digital_7/fonts.css"></style>
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
import reception from "./views/receptionView/reception";
import receptionMain from "./views/receptionView/receptionMain";
import receptionLogin from "./views/receptionView/receptionLogin";
import receptionSearch from "./views/receptionView/receptionSearch";
import receptionSettings from "./views/receptionView/receptionSettings";

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
    'reception': reception,
    'receptionMain': receptionMain,
    'receptionLogin': receptionLogin,
    'receptionSearch': receptionSearch,
    'receptionSettings': receptionSettings,

  },
  mounted() {

  },
  beforeDestroy() {

  },
  methods: {}
}
</script>
