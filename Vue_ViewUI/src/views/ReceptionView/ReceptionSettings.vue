<template>
  <div class="tabBase">
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>前台</BreadcrumbItem>
      <BreadcrumbItem>设置</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <Row>
        <Col :xs="24" :sm="16" :md="12" :lg="10" :xl="8" :xxl="6">
          <CellGroup>
            <Cell class="settings" title="前台登出">
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
  name: "receptionSettings"
}
</script>

<style scoped src="../../styles/settings.css"></style>
<style scoped>

</style>