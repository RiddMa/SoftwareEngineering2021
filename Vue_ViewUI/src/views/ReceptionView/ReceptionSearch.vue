<template>
	<div class="tabBase">
		<Breadcrumb :style="{margin: '16px  1%'}">
			<BreadcrumbItem>管理员</BreadcrumbItem>
			<BreadcrumbItem>房间查询</BreadcrumbItem>
		</Breadcrumb>
		<Card>
			<Row class="searchContent">
				<Col :lg="10" :md="12" :sm="16" :xl="8" :xs="24" :xxl="6">
					<CellGroup>
						<Form>
							<FormItem>
								<Input v-model="searchText" placeholder="请输入房间号..." size="large" type="text">
									<Icon slot="prepend" type="ios-person-outline"></Icon>
								</Input>
							</FormItem>
						</Form>
						<Cell class="settings" title="查询账单">
							<Button slot="extra" shape="circle" type="primary" @click="getInvoice(searchText)">查询</Button>
						</Cell>
						<Cell class="settings" title="查询详单">
							<Button slot="extra" shape="circle" type="primary" @click="getDetailedList(searchText)">查询</Button>
						</Cell>
					</CellGroup>
				</Col>
			</Row>
			<div v-if="showInvoice">
				<Row class="searchContent">
					<div id="invoice" style="width:100%;margin: 4vh 0">
						<Table :columns="invoiceColumns" :data="invoiceData" stripe></Table>
					</div>
				</Row>
				<Row class="searchContent">
					<Button v-print="printInvoice" shape="circle" size="large" type="primary">打印账单</Button>
				</Row>
			</div>
			<div v-if="showDetailedList">
				<Row class="searchContent">
					<div id="detailedList" style="width:100%;margin: 4vh 0">
						<Table :columns="detailedListColumns" :data="detailedListData" stripe></Table>
					</div>
				</Row>
				<Row class="searchContent">
					<Button v-print="printDetailedList" shape="circle" size="large" type="primary">打印详单</Button>
				</Row>
			</div>


			<!--      <div class="searchResult" v-if="hasSearched">-->
			<!--        <Row>-->
			<!--          <Col :xs="24" :sm="12" :md="12" :lg="8" :xl="6" :xxl="4" v-for="item in this.resultRoom"-->
			<!--               v-bind:key="item.rid">-->
			<!--            <Card class="acCard">-->
			<!--              <Row slot="title">-->
			<!--                <Col class="acCardTitle" :span="20">-->
			<!--                  <h3 class="acCardTitleText">房间{{ item.rid }}</h3>-->
			<!--                </Col>-->
			<!--                <Col align="end" :span="4">-->
			<!--                  <Button icon="ios-information-circle-outline" shape="circle"-->
			<!--                          @click="printDetailedList($event,item.rid)"></Button>-->
			<!--                </Col>-->
			<!--              </Row>-->

			<!--              <Row class="acCardContent">-->
			<!--                <Col :span="12">-->
			<!--                  <span>当前状态：</span>-->
			<!--                </Col>-->
			<!--                <Col align="end" :span="12">-->
			<!--                  <Switch v-model="item.power" size="large" type="primary" shape="circle">-->
			<!--                    <span slot="open">ON</span>-->
			<!--                    <span slot="close">OFF</span>-->
			<!--                  </Switch>-->
			<!--                </Col>-->
			<!--              </Row>-->
			<!--              <Row class="acCardContent">-->
			<!--                <Col :span="12">-->
			<!--                  <span>累计金额：</span>-->
			<!--                </Col>-->
			<!--                <Col align="end" :span="12">-->
			<!--                  <span><b>￥{{ item.cost }}</b></span>-->
			<!--                </Col>-->
			<!--              </Row>-->

			<!--            </Card>-->
			<!--          </Col>-->
			<!--        </Row>-->
			<!--      </div>-->
		</Card>
	</div>
</template>

<script>
import {NetworkController} from "../../libs/NetworkController";

export default {
	name: "ReceptionSearch",
	data: function () {
		return {
			showInvoice: false,
			showDetailedList: false,
			searchText: '',
			printInvoice: {
				id: 'invoice',
				popTitle: '空调使用账单',
			},
			printDetailedList: {
				id: 'detailedList',
				popTitle: '空调使用详单',
			}
		}
	},
	computed: {
		//账单表格格式
		invoiceColumns: {
			get: function () {
				return [
					{
						title: '房间号',
						key: 'roomId'
					},
					{
						title: '总金额',
						key: 'totalFee'
					},
					{
						title: '入住时间',
						key: 'dateIn'
					},
					{
						title: '退房时间',
						key: 'dateOut'
					}
				];
			},
			set: function () {

			}
		},
		invoiceData: {
			get: function () {
				return this.$store.state.invoice;
			},
			set: function () {

			}
		},
		//详单表格格式
		detailedListColumns: {
			get: function () {
				return [
					{
						title: '房间号',
						key: 'roomId'
					},
					{
						title: '请求时刻',
						key: 'requestTime'
					},
					{
						title: '请求时长',
						key: 'requestDuration'
					},
					{
						title: '风速',
						key: 'fanSpeed'
					},
					{
						title: '费用速率',
						key: 'feeRate'
					},
					{
						title: '产生费用',
						key: 'fee'
					},
				];
			},
			set: function () {
			}
		},
		detailedListData: {
			get: function () {
				return this.$store.state.detailedList;
			},
			set: function () {
			}
		},
	},
	methods: {
		async getInvoice(roomId) {
			if (roomId !== '') {
				let nc = NetworkController.getInstance();
				let errCode = await nc.createInvoice(this, roomId);
				if (errCode === 0) {
					this.showInvoice = true;
					// this.showDetailedList = false;
				}
			} else {

			}
		},
		async getDetailedList(roomId) {
			if (roomId !== '') {
				let nc = NetworkController.getInstance();
				let errCode = await nc.createDetailedList(this, roomId);
				if (errCode === 0) {
					this.showDetailedList = true;
					// this.showInvoice = false;
				}
			} else {

			}
		},
	}
}
</script>

<style scoped src="../../styles/search.css"></style>
<style scoped>

</style>