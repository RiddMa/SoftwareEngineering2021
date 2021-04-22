<template>
  <div>
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>管理员</BreadcrumbItem>
      <BreadcrumbItem>房间查询</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <Input class="adminSearch" size="large" search enter-button placeholder="请输入房间号..." />

    </Card>
  </div>
</template>

<script>
export default {
  name: "adminSearch"
}
</script>

<style scoped>
.adminSearch{
  alignment: center;
  max-width: 720px;
  margin: 0 auto;
}
</style>