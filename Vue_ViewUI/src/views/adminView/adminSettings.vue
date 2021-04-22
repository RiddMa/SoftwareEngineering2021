<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>设置</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <span>中央空调控制</span>
      <Switch :before-change="handleBeforeChangeCAC" v-model="this.$store.state.CACState" size="large" type="primary" shape="circle">
        <span slot="open">ON</span>
        <span slot="close">OFF</span>
      </Switch>
    </Card>
  </div>
</template>

<script>
export default {
  name: "adminSettings",
  methods: {
    handleBeforeChangeCAC() {
      return new Promise((resolve) => {
        if (this.$store.state.CACState === true) {
          this.$Modal.confirm({
            title: '关机',
            content: '您确认要关闭中央空调吗？',
            onOk: () => {
              this.$store.state.CACState=false;
              resolve();
            }
          });
        } else {
          this.$Modal.confirm({
            title: '开机',
            content: '您确认要开启中央空调吗？',
            onOk: () => {
              this.$store.state.CACState=true;
              resolve();
            }
          });
        }

      });
    }
  }
}
</script>

<style scoped>

</style>