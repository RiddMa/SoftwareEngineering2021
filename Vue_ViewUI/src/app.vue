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
import Admin from './views/AdminView/Admin.vue';
import ClientLogin from "./views/ClientView/ClientLogin.vue";
import Client from "./views/ClientView/Client.vue";
import NetInterfaceTest from "./views/NetInterfaceTest";
import Welcome from "./views/Welcome";
import connect_token from "./connect_token"
import Vue from "vue";
import AdminLogin from "./views/AdminView/AdminLogin";
import AdminMain from "./views/AdminView/AdminMain";
import AdminSearch from "./views/AdminView/AdminSearch";
import AdminSettings from "./views/AdminView/AdminSettings";
import Reception from "./views/ReceptionView/Reception";
import ReceptionMain from "./views/ReceptionView/ReceptionMain";
import ReceptionLogin from "./views/ReceptionView/ReceptionLogin";
import ReceptionSearch from "./views/ReceptionView/ReceptionSearch";
import ReceptionSettings from "./views/ReceptionView/ReceptionSettings";
import Manager from "./views/ManagerView/Manager";
import ManagerSettings from "./views/ManagerView/ManagerSettings";
import ManagerLogin from "./views/ManagerView/ManagerLogin";
import ManagerDaily from "./views/ManagerView/ManagerDaily";
import ManagerWeekly from "./views/ManagerView/ManagerWeekly";
// import NetworkController from "./libs/NetworkController";

export default {
  data() {
    return {}
  },
  components: {
    'Welcome': Welcome,
    'NetInterfaceTest': NetInterfaceTest,
    'connect_token': connect_token,
    'Admin': Admin,
    'AdminLogin': AdminLogin,
    'AdminMain': AdminMain,
    'AdminSearch': AdminSearch,
    'AdminSettings': AdminSettings,
    'ClientLogin': ClientLogin,
    'Client': Client,
    'Reception': Reception,
    'ReceptionMain': ReceptionMain,
    'ReceptionLogin': ReceptionLogin,
    'ReceptionSearch': ReceptionSearch,
    'ReceptionSettings': ReceptionSettings,
    'Manager': Manager,
    'ManagerLogin': ManagerLogin,
    'ManagerDaily': ManagerDaily,
    'ManagerWeekly': ManagerWeekly,
    'ManagerSettings': ManagerSettings
  },
  mounted() {
    // this.networkController = Network
  },
  beforeDestroy() {

  },
  methods: {}
}
</script>
