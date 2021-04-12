<style scoped>
/*.ivu-layout-sider-children{*/
/*  background:#001529;*/
/*}*/
/*.ivu-layout-sider{*/
/*  background:#001529;*/
/*}*/
/*.ivu-layout-sider-trigger{*/
/*  background:#001529;*/
/*  color:#001529;*/
/*}*/
/*.ivu-menu-dark{*/
/*  background:#001529;*/
/*}*/
/*.ivu-menu{*/
/*  color:#001529;*/
/*}*/

.layout-con{
  height: 100%;
  width: 100%;
}
.menu-item span{
  display: inline-block;
  overflow: hidden;
  width: 100px;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
  transition: width .2s ease .2s;

}
.menu-item i{
  transform: translateX(0px);
  transition: font-size .2s ease, transform .2s ease;
  vertical-align: middle;
  font-size: 16px;
}
.collapsed-menu span{
  width: 0px;
  transition: width .2s ease;
}
.collapsed-menu i{
  transform: translateX(5px);
  transition: font-size .2s ease .2s, transform .2s ease .2s;
  vertical-align: middle;
  font-size: 22px;
}
.SiderText{
  font-size: large;
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;

}
</style>
<template>
  <div class="layout">
    <Layout :style="{minHeight: '100vh'}">
      <Sider collapsible :collapsed-width="80" v-model="isCollapsed">
        <Menu active-name="1-1" theme="dark" width="auto" :class="menuitemClasses">
          <MenuItem name="1-1">
            <Icon type="ios-apps"></Icon>
            <span class="SiderText">空调概览</span>
          </MenuItem>
          <MenuItem name="1-2">
            <Icon type="ios-search"></Icon>
            <span class="SiderText">房间查询</span>
          </MenuItem>
          <MenuItem name="1-3">
            <Icon type="ios-settings"></Icon>
            <span class="SiderText">偏好设置</span>
          </MenuItem>
        </Menu>
      </Sider>
      <Layout>
        <Header :style="{background: '#fff', boxShadow: '0 2px 3px 2px rgba(0,0,0,.1)'}">
          <h2>酒店空调管理系统</h2>
        </Header>
        <Content :style="{padding: '0 16px 16px'}">
          <Breadcrumb :style="{margin: '16px  1%'}">
            <BreadcrumbItem>空调概览</BreadcrumbItem>
            <BreadcrumbItem>Components</BreadcrumbItem>

          </Breadcrumb>
          <Card>
            <div style="height: 600px">Content</div>
          </Card>
        </Content>
      </Layout>
    </Layout>
  </div>
</template>
<script>
export default {
  data () {
    return {
      isCollapsed: false
    };
  },
  computed: {
    menuitemClasses: function () {
      return [
        'menu-item',
        this.isCollapsed ? 'collapsed-menu' : ''
      ]
    }
  }
}
</script>
