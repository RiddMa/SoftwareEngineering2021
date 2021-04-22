<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>空调概览</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <div class="acList">
        <Row>
          <Col :xs="24" :sm="12" :md="12" :lg="8" :xl="6" :xxl="4" v-for="item in this.$store.state.roomInfo">
            <Card class="acCard">
              <h3 class="acCardTitle" slot="title">房间{{ item.rid }}</h3>
              <Poptip slot="extra" placement="right" width="400">
                <Button icon="ios-settings" shape="circle" style="{padding-bottom:5px}"></Button>
                <div class="api" slot="content">
                  <table>
                    <thead>
                    <tr>
                      <th>Version</th>
                      <th>Update Time</th>
                      <th>Description</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                      <td>0.9.5</td>
                      <td>2016-10-26</td>
                      <td>Add new components <code>Tooltip</code> and <code>Poptip</code></td>
                    </tr>
                    <tr>
                      <td>0.9.4</td>
                      <td>2016-10-25</td>
                      <td>Add new components <code>Modal</code></td>
                    </tr>
                    <tr>
                      <td>0.9.2</td>
                      <td>2016-09-28</td>
                      <td>Add new components <code>Select</code></td>
                    </tr>
                    </tbody>
                  </table>
                </div>
              </Poptip>
              <span>当前温度：</span>
              <Button icon="ios-arrow-down" shape="circle" @click="changeTemp($event,item.curnTemp,-1)"></Button>
              <span>{{ item.curnTemp }}</span>
              <Button icon="ios-arrow-up" shape="circle"></Button>
              <br>
              <span>当前风速：</span>
              <Button icon="md-remove" shape="circle"></Button>
              <span>{{ item.curnWind }}</span>
              <Button icon="md-add" shape="circle"></Button>
              <br>
              <span>当前模式：</span>
              <Button v-if="item.curnMode==='致冷'" type="primary" icon="ios-snow" shape="circle"
                      @click="changeMode($event,'致冷')"></Button>
              <Button v-else icon="ios-snow" shape="circle" @click="changeMode($event,'致冷')"></Button>
              <span>{{ item.curnMode }}</span>
              <Button v-if="item.curnMode==='制热'" type="primary" icon="ios-sunny" shape="circle"
                      @click="changeMode($event,'制热')"></Button>
              <Button v-else icon="ios-sunny" shape="circle" @click="changeMode($event,'制热')"></Button>
              <br>

            </Card>
          </Col>
        </Row>
      </div>
    </Card>
  </div>
</template>

<script>
export default {
  name: "adminMain",
  data: function () {
    return {}
  },
  methods: {
    popSettings(e, rid) {

    },
    changeTemp: function (e, turnUp) {

    },
    changeMode: function (e, toMode) {

    },
  }
}
</script>

<style scoped>
.acCard {
  margin: 0.8vh 0.8vw;
}
.acCardTitle{
  display: inline-block;
  overflow: hidden;
  width: 80%;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: middle;
  transition: width .2s ease .2s;
}

</style>