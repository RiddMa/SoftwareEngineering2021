<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>空调概览</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <div v-for="i in 12">
        <Row>
          <div v-for="j in 4">
            <Col :span="6">
              <p> {{i}},{{j}} </p>
            </Col>
          </div>
        </Row>
      </div>

      <div class="acList" v-for="i in 3">
        <Row>
          <Col v-for="j in 3" :span="8">
            <Card class="acCard">
              <p slot="title">房间{{ i.rid }}</p>
              <Icon type="ios-settings" slot="extra"></Icon>
              <p>当前温度：{{ i.curnTemp }}</p>
              <p>当前风速：{{ i.curnWind }}</p>
            </Card>
          </Col>
        </Row>
      </div>
    </Card>
  </div>
</template>

<script>
export default {
  name: "adminMain"
}
</script>

<style scoped>
.acCard {
  width: 300px;
  margin-top: 1vh;
  margin-bottom: 1vh;
}
</style>