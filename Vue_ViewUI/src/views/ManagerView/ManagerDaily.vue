<template>
	<div class="tabBase">
		<Breadcrumb :style="{margin: '16px  1%'}">
			<BreadcrumbItem>经理</BreadcrumbItem>
			<BreadcrumbItem>日报</BreadcrumbItem>
		</Breadcrumb>
		<Card>
			<Row>
				<Col :lg="10" :md="12" :sm="16" :xl="8" :xs="24" :xxl="6">
					<Form>
						<FormItem>
							<Input v-model="searchText" placeholder="请输入房间号..." size="large" type="text">
								<Icon slot="prepend" type="ios-person-outline"></Icon>
							</Input>
						</FormItem>
						<FormItem>
							<Row>
								<Col span="12">
									<DatePicker v-model="queryDateRange" :options="datePickerOptions" :start-date="startDate" clearable
									            format="yyyy/MM/dd"
									            placeholder="请选择日期" size="large" split-panels
									            type="daterange"></DatePicker>
								</Col>
								<Col span="12" style="vertical-align: center;text-align: right">
									<Button shape="circle" type="primary" @click="getReport(searchText)">查询报表</Button>
								</Col>
							</Row>

						</FormItem>
					</Form>
				</Col>
			</Row>
			<div v-if="hasResult">
				<div id="canvas"></div>
				<div id="roomReport" style="width:100%;margin: 4vh 0">
					<Table :columns="roomReportColumns" :data="roomReportData" stripe></Table>
				</div>
			</div>
			<div id="feePlot"></div>


		</Card>
	</div>
</template>

<script>
import Vue from "vue";
import {NetworkController} from "../../libs/NetworkController";
import {Histogram} from "@antv/g2plot";

const moment = require('moment');

const g2plot = require('@antv/g2plot'); // 1. 引入g2plot
Vue.$g2plot = g2plot; // 2. 将g2plot挂载到vue中
export default {
	name: "ManagerDaily",
	data: function () {
		return {
			searchText: '',
			hasResult: false,
			queryDateRange: [],
			startDate: moment().subtract(1, 'months').toDate(),
			datePickerOptions: {
				disabledDate(date) {
					return date && date.valueOf() > Date.now();
				},
				shortcuts: [
					{
						text: '近一周',
						value() {
							const end = new Date();
							const start = moment().subtract(1, 'weeks').toDate();
							return [start, end];
						}
					},
					{
						text: '近一月',
						value() {
							const end = new Date();
							const start = moment().subtract(1, 'months').toDate();
							return [start, end];
						}
					},
					{
						text: '近三月',
						value() {
							const end = new Date();
							const start = moment().subtract(3, 'months').toDate();
							return [start, end];
						}
					},
					{
						text: '近半年',
						value() {
							const end = new Date();
							const start = moment().subtract(6, 'months').toDate();
							return [start, end];
						}
					},
					{
						text: '近一年',
						value() {
							const end = new Date();
							const start = moment().subtract(1, 'years').toDate();
							return [start, end];
						}
					},
				]
			},
			mockData: [
				{year: '1991', value: 3},
				{year: '1992', value: 4},
				{year: '1993', value: 3.5},
				{year: '1994', value: 5},
				{year: '1995', value: 4.9},
				{year: '1996', value: 6},
				{year: '1997', value: 7},
				{year: '1998', value: 9},
				{year: '1999', value: 13}
			]
		}
	},
	computed: {
		roomReportColumns: {
			get: function () {
				return [
					{
						title: '房间号',
						key: 'roomId'
					},
					{
						title: '总费用',
						key: 'totalFee'
					},
					{
						title: '空调工作时长',
						key: 'acWorkingTime'
					},
					{
						title: '详单条数',
						key: 'detailedListNum'
					},
					{
						title: '调温次数',
						key: 'changeTempTimes'
					},
					{
						title: '调风次数',
						key: 'changeSpeedTimes'
					},
					{
						title: '关机次数',
						key: 'powerOffTimes'
					},
				]
			},
			set: function () {
			},
		},
		roomReportData: {
			get: function () {
				return this.$store.state.managerReport;
			},
			set: function () {
			},
		},
	},
	methods: {
		async getReport(roomId) {
			if (roomId !== '') {
				let nc = NetworkController.getInstance();
				let errCode = await nc.createReport(this, roomId, this.queryDateRange);
				if (errCode === 0) {
					this.hasResult = true;
				} else {
					this.hasResult = false;
				}
			} else {
				this.hasResult = false;

			}
		},
	},
	mounted() {
		const linePlot = new Vue.$g2plot.Line('canvas', {
			data: this.mockData,
			xField: 'year',
			yField: 'value'
		})
		linePlot.render()
		// const histogramPlot = new Histogram('feePlot',{
		// 	data:objArray.map(this.roomReportData => this.roomReportData.totalFee),
		// 	binField:'totalFee',
		// })
	}
}
</script>

<style scoped>

</style>