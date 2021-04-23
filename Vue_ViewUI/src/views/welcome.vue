<template>
  <div id="nav">
    <Row type="flex" justify="center" align="middle">
      <Col span="12">
        <Card class="WelcomeNav">
          <router-link to="/client/login">
            <h1>
              <Icon type="ios-contacts"/>
              Client
            </h1>
          </router-link>
          <router-link to="/admin/login">
            <h1>
              <Icon type="ios-contact"/>
              Admin
            </h1>
          </router-link>
          <router-link to="/reception/login">
            <h1>
              <Icon type="ios-desktop"/>
              Reception
            </h1>
          </router-link>
          <router-link to="/reception/login">
            <h1>
              <Icon type="ios-glasses" />
              Manager
            </h1>
          </router-link>
        </Card>
      </Col>
    </Row>

  </div>
</template>

<script>
export default {
  name: "welcome"
}
</script>

<style scoped>
.WelcomeNav {
  margin-top: 10%;
  margin-bottom: 10%;
}
</style>