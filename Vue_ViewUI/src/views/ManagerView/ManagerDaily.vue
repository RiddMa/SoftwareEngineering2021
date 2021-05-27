<template>
  <div class="tabBase">
    <Breadcrumb :style="{margin: '16px  1%'}">
      <BreadcrumbItem>经理</BreadcrumbItem>
      <BreadcrumbItem>日报</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <div id="canvas"></div>
    </Card>
  </div>
</template>

<script>
import Vue from "vue";
const g2plot = require('@antv/g2plot') // 1. 引入g2plot
Vue.$g2plot=g2plot
export default {
  name: "ManagerDaily",
  data () {
    return {
      mockData: [
        { year: '1991', value: 3 },
        { year: '1992', value: 4 },
        { year: '1993', value: 3.5 },
        { year: '1994', value: 5 },
        { year: '1995', value: 4.9 },
        { year: '1996', value: 6 },
        { year: '1997', value: 7 },
        { year: '1998', value: 9 },
        { year: '1999', value: 13 }
      ]
    }
  },
  mounted() {
    const linePlot = new Vue.$g2plot.Line('canvas', {
      data: this.mockData,
      xField: 'year',
      yField: 'value'
    })
    linePlot.render()
  }
}
</script>

<style scoped>

</style>