<template>
  <div class="layout">
    <Header class="aHeader">
      <h2 class="aHeaderContent">
        酒店空调管理系统
        <Button type="primary" shape="circle" @click="addAC($event)">[测试用]添加空调</Button>
      </h2>
      <Menu class="aMenu" mode="horizontal" active-name="1">
        <MenuItem name="1" to="/reception/main">
          <Icon type="ios-apps"></Icon>
          <span class="MenuText">顾客登记</span>
        </MenuItem>
        <MenuItem name="2" to="/reception/search">
          <Icon type="ios-search"></Icon>
          <span class="MenuText">房间查询</span>
        </MenuItem>
        <MenuItem name="3" to="/reception/settings">
          <Icon type="ios-settings"></Icon>
          <span class="MenuText">偏好设置</span>
        </MenuItem>
      </Menu>
    </Header>
    <Content :style="{padding:'0 5vw 0 5vw'}">
      <div :style="{padding: '60px'}"></div>
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
    </Content>
  </div>
</template>

<script>
export default {
  name: "reception"
}
</script>

<style scoped src="../../styles/header.css"></style>
<style scoped>

</style>