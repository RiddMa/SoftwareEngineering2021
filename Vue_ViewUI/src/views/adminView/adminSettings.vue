<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>设置</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <Row>
        <Col :xs="24" :sm="16" :md="12" :lg="10" :xl="8" :xxl="6">
          <CellGroup>
            <Cell class="settings" title="中央空调控制">
              <Switch slot="extra" :before-change="handleBeforeChangeCAC" v-model="this.$store.state.CACState"
                      size="large" type="primary" shape="circle">
                <span slot="open">ON</span>
                <span slot="close">OFF</span>
              </Switch>
            </Cell>
            <Cell class="settings" title="管理员登出">
              <Button slot="extra" type="error" shape="circle" @click="adminLogout($event,adminId)">登出</Button>
            </Cell>
          </CellGroup>

        </Col>

      </Row>
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
              this.$store.state.CACState = false;
              resolve();
            }
          });
        } else {
          this.$Modal.confirm({
            title: '开机',
            content: '您确认要开启中央空调吗？',
            onOk: () => {
              this.$store.state.CACState = true;
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
.settings {
  margin: 2vh 0;
}

</style>