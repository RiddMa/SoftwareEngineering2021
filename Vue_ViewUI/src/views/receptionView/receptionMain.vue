<template>
  <div class="tabBase">
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>前台</BreadcrumbItem>
      <BreadcrumbItem>顾客登记</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <Form class="checkInForm" ref="formInline" :model="formInline" :rules="ruleInline" inline>
        <FormItem prop="phone">
          <Input type="text" v-model="formInline.phone" placeholder="请输入手机号……">
            <Icon type="ios-person-outline" slot="prepend"></Icon>
          </Input>
        </FormItem>
        <FormItem>
          <Button type="primary" shape="circle" @click="handleSubmit('formInline')">登记</Button>
        </FormItem>
      </Form>
    </Card>
  </div>
</template>

<script>
export default {
  name: "receptionMain",

  data () {
    return {
      formInline: {
        phone: '',
      },
      ruleInline: {
        phone: [
          { required: true, message: '手机号不能为空', trigger: 'blur' }
        ],
      }
    }
  },
  methods: {
    handleSubmit(name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.$Message.success('Success!');
        } else {
          this.$Message.error('Fail!');
        }
      })
    }
  },
}
</script>

<style scoped>
.tabBase{

}
.checkInForm{
  margin: 2vh 2vw;
}

</style>