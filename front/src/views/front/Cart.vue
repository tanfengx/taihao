<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onMounted, reactive, ref} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // 引入 css
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
  import config from "../../../config";

  const userStore = useUserStore()
  const user = userStore.getUser
  //判断用户是否登录
  if(user.id==null){
      router.push('/login')
  }else{
      const token = userStore.getBearerToken
      const auths =  userStore.getAuths
  }
  const pageNum = ref(1)
  const pageSize = ref(5)
  const total = ref(0)

    //判断用户是否登录
  if(user.id==null){
      router.push('/login')
  }

  const content = ref('')
  const viewShow = ref(false)
  const view = (value) => {
    viewShow.value = true
    content.value = value
  }

  const id = router.currentRoute.value.query.id
  let name = router.currentRoute.value.query.name
  const state = reactive({
    tableData:[],
  })

  const load = () => {
    request.get('/front/cart/list').then(res => {
      state.tableData = res.data
      state.tableData = state.tableData.filter((item) => item.userId === user.id);

    })
  }
  load()  // 调用 load方法拿到后台数据

  //轮播图
  request.get('/front/banner/list').then(res => {
      state.rotationList = res.data
      state.rotationList = state.rotationList.filter((item) => item.indexRadio === '否');
  })

  //计算购物车总价
  const getTotalPrice =() =>{
      const totalPrice = state.tableData.reduce((sum, item) => {
          return sum + item.price*item.num;
      }, 0);
      return totalPrice.toFixed(2);
  }

  //修改购物车
  const changeNum = (row) =>{
      request.request({
          url: '/front/cart/update',
          method: 'post',
          data: {
              id:row.id,
              name:row.name,
              userId:user.id,
              num:row.num,
          }
      }).then(res => {
          seats.selectedSeats = []
          if (res.code === '200') {
              ElMessage.success('修改成功')
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  //删除购物车
  const deleteCart =(id) =>{
      request.delete('/front/cart/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('操作成功')
              load()  // 刷新表格数据
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  //批量删除购物车
  const deleteBatchCart =(ids) =>{
      ids.forEach((e)=>{
          request.delete('/front/cart/' + e).then(res => {})
      })
  }

  //收货地址
  state.selectedAddress = '';
  state.addressList = []
  request.get('/front/address/list').then(res => {
      state.addressList = res.data
      state.addressList = state.addressList.filter((item) => item.userId === user.id);
      const selectAddress = state.addressList.filter((item) => item.defaultRadio === '是');
      if(selectAddress!=null){
          state.selectedAddress = selectAddress[0].id
      }
  })

  //支付方式
  state.selectedPaytype = 1;
  state.payTypeList = []
  request.get('/front/paytype/list').then(res => {
      state.payTypeList = res.data
  })

  //去结算
  const dialogFormVisible = ref(false)
  state.qrcode = ''
  const toOrder = () =>{
      const flag = validateForm()
      if(!flag)return;

      dialogFormVisible.value = true
      const selectPaytype = state.payTypeList.filter((item) => item.id === state.selectedPaytype);
      if(selectPaytype!=null){
          state.qrcode = selectPaytype[0].img
      }
  }

  const validateForm = () =>{
      if(state.tableData.length==0){
          ElMessage.error('购物车为空！请先添加')
          return false;
      }
      if(state.addressList.length==0){
          ElMessage.error('收货地址为空！请先添加')
          return false;
      }
      if(state.payTypeList.length==0){
          ElMessage.error('支付方式为空！请先添加')
          return false;
      }
      return true
  }

  state.orders = {}
  state.pList = ``
  //保存订单
  const saveOrder = () =>{
      const flag = validateForm()
      if(!flag)return;

      const groups = state.tableData.reduce((acc, cur) => {
          const bizUser = cur.bizUserId;
          if (!acc[bizUser]) {
              acc[bizUser] = [];
          }
          acc[bizUser].push(cur);
          return acc;
      }, {});
      const result = Object.values(groups);

      result.forEach((array)=>{
          state.pList = ``

          state.orders.name = generateOrderNumber()
          const selectAddress = state.addressList.filter((item) => item.id === state.selectedAddress);
          const selectedPaytype = state.payTypeList.filter((item) => item.id === state.selectedPaytype);
          state.pList = `收货地址：${selectAddress[0].name}，${selectAddress[0].phone}，${selectAddress[0].address}<br/>`;
          state.pList += `支付方式：${selectedPaytype[0].name}<br/>`;
          state.pList += `商品明细：<br/>`;
          state.pList += `<ul>`
          const goodids = [];
          array.forEach((e,i)=>{
              goodids.push(e.goodid)
              state.pList += `<li>商品：${e.name}，数量：${e.num}，单价：${e.price}</li>`
          })
          state.orders.goodids = goodids.join(',');
          state.pList += `</ul>`
          state.orders.content = state.pList
          state.orders.stateRadio = '已下单'
          state.orders.userId = user.id
          state.orders.amount = array.reduce((acc, item) => {
              return acc + (item.price * item.num);
          }, 0).toFixed(2);
          if(user.isvip=='是'){
            state.orders.amount = parseFloat(state.orders.amount*0.9).toFixed(2)
          }
          state.orders.bizUserId = array[0].bizUserId
          request.request({
              url: '/front/orders/update',
              method: 'post',
              data: state.orders
          }).then(res => {
              if (res.code === '200') {
                  dialogFormVisible.value = false;
                  //清空购物车车数据
                  const ids = state.tableData.map(obj => obj.id);
                  deleteBatchCart(ids)

                  router.push('/front/orders')
              } else {
                  ElMessage.error(res.msg)
              }
          })
      });

  }

  //生成订单号
  function generateOrderNumber() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const seconds = String(date.getSeconds()).padStart(2, '0');
      const orderNumber = `${year}${month}${day}${hours}${minutes}${seconds}`;
      return orderNumber;
  }

  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)



</script>

<template>
  <div>

          <!-- 轮播图 -->
          <div style="margin-top: 10px;">
              <div style="width: 80%;margin: 0 auto;">
                      <el-carousel :interval="5000" arrow="always" height="200px">
                          <el-carousel-item v-for="item in state.rotationList" :key="item">
                              <a :href="item.url" target="_blank"><img :src="item.img" alt="" style="width: 100%; height: 100%"></a>
                          </el-carousel-item>
                      </el-carousel>
              </div>
          </div>


      <div style="width:80%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 15px ;margin-top: 20px;text-align: left;">
            <span style="font-size: 14px;margin-right: 20px;">首页 > 购物车</span>
        </div>

          <div style="display: flex; align-items: center; justify-content: center; padding-bottom: 15px; text-align: center; line-height: 40px;">
              <span style="font-weight: bold; font-size: 22px;margin-left:10px;">购物车</span>
          </div>

          <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" :header-cell-class-name="'headerBg'">
            <el-table-column prop="id" label="序号" width="80px;">
                <template #default="scope">
                    {{ scope.$index + 1 }}
                </template>
                </el-table-column>
                <el-table-column label="商品图片" width="120px;">
                    <template #default="scope" >
                        <img :src="scope.row.img" alt="商品图片" style="width: 100px; height: 80px;">
                    </template>
                </el-table-column>
                <el-table-column prop="name" label="名称" width="320px;"></el-table-column>
                <el-table-column label="商户" width="160px;">
                    <template #default="scope">
                        <span v-if="scope.row.bizUserId">{{ state.userOptions.find(v => v.id === scope.row.bizUserId) ? state.userOptions.find(v => v.id === scope.row.bizUserId).name : '' }}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="price" label="价格">
                    <template #default="scope" >
                        <span style="font-size: 16px;">￥{{scope.row.price}}</span>
                    </template>
                </el-table-column>
                <el-table-column prop="num" label="数量" width="180px;">
                  <template #default="scope">
                    <el-input-number
                        v-model="scope.row.num"
                        :min="1"
                        :max="100"
                        @change="changeNum(scope.row)"
                    ></el-input-number>
                  </template>
                </el-table-column>
                <el-table-column label="小计">
                    <template #default="scope">
                        <span style="font-size: 16px;">￥{{ (scope.row.price*scope.row.num).toFixed(2)}}</span>
                    </template>
                </el-table-column>


                <el-table-column label="操作">
                    <template #default="scope">
                        <el-button type="danger" size="small" @click="deleteCart(scope.row.id)">删除</el-button>
                    </template>
                </el-table-column>
        </el-table>

        <div class="total-container">
          <span class="total-label">合计：</span>
          <span class="total-price">￥{{ getTotalPrice() }}</span>
        </div>
        <div class="total-container" v-if="user.isvip=='是'">
          <span class="total-label">你是网站会员，享受9折优惠，优惠后总价：</span>
          <span class="total-price">￥{{ parseFloat(getTotalPrice()*0.9).toFixed(2) }}</span>
        </div>





              <!-- 选择收货地址 -->
              <div class="address-list" style="margin-top: 30px;">
                  <div style="display: flex; align-items: center; justify-content: center; padding-bottom: 15px; text-align: center; line-height: 40px;">
                      <span style="font-weight: bold; font-size: 22px;margin-left:10px;">选择收货地址</span>
                  </div>
                  <div style="margin-top: 10px;text-align: right;">
                      <el-button type="info" plain @click="router.push('/front/address')">修改收货地址</el-button>
                  </div>
                  <ul style="margin-top: 15px;">
                      <li>
                          <div class="address-item">
                              <span style="font-weight: bold;">姓名</span>
                              <span style="font-weight: bold;">手机号码</span>
                              <span style="font-weight: bold;">详情地址</span>
                          </div>
                      </li>
                      <li v-for="address in state.addressList" :key="address.id">
                          <div class="address-item">
                              <span><el-radio v-model="state.selectedAddress" :label="address.id">{{address.name}}</el-radio></span>
                              <span>{{ address.phone }}</span>
                              <span>{{ address.address }}</span>
                          </div>
                      </li>
                  </ul>
              </div>

          <!-- 选择支付方式 -->
          <div class="pay-list" style="margin-top: 30px;">
              <div style="display: flex; align-items: center; justify-content: center; padding-bottom: 15px; text-align: center; line-height: 40px;">
                  <span style="font-weight: bold; font-size: 22px;margin-left:10px;">请选择支付方式</span>
              </div>
              <div style="margin-top: 15px;text-align: center;">
                  <el-radio-group v-model="state.selectedPaytype">
                      <el-radio v-for="paytype in state.payTypeList" :label="paytype.id" >
                          {{paytype.name}}
                      </el-radio>
                  </el-radio-group>
              </div>
          </div>

          <div style="display: flex; justify-content: center; align-items: center; height: 100%;margin-top: 50px;">
              <el-button type="primary" @click="toOrder" size="large">确认</el-button>
          </div>
    </div>

      <!-- 支付框 -->
    <el-dialog v-model="dialogFormVisible" title="确认支付" width="40%">
        <div style="text-align: center;" v-if="user.isvip=='是'">
            总金额：<span style="font-size: 25px;color: red;">￥{{ parseFloat(getTotalPrice()*0.9).toFixed(2) }}</span><span style="margin-left: 20px;">请扫码二维码</span>
        </div>
        <div style="text-align: center;" v-else>
            总金额：<span style="font-size: 25px;color: red;">￥{{ getTotalPrice() }}</span><span style="margin-left: 20px;">请扫码二维码</span>
        </div>
        <div style="margin-top: 10px;text-align: center;">
            <img :src="state.qrcode" alt="支付二维码" style="width: 200px;height: 220px;">
        </div>
        <div style="margin-top: 10px;text-align: center;">
            <el-button type="primary" @click="saveOrder">确认购买</el-button>
        </div>
    </el-dialog>

  </div>
</template>

<style>
    .address-list {
        width: 100%;
        margin: 0 auto;
        padding: 20px;
    }

    .order-list {
        width: 100%;
        margin: 0 auto;
        padding: 20px;
    }

    .address-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
        cursor: pointer;
        text-align: center;
    }

    .address-list ul {
        list-style-type: none;
        padding: 0;
    }

    .address-list li {
        padding: 8px;
        cursor: pointer;
        border-radius: 10px;
    }

    .address-list li:hover {
        background-color: #efefef;
    }
    .total-container {
        margin-top: 20px;
        text-align: right;
        margin-right: 20px;
    }

    .total-label {
        font-weight: bold;
    }

    .total-price {
        color: red;
        font-size: 25px;
        font-weight: bold;

    }

    a.delete-link {
        color: #ff0000;
        text-decoration: none;
    }

    a.delete-link:hover {
        text-decoration: underline;
    }


    .pay-list {
        width: 100%;
        margin: 0 auto;
        display: flow;
    }

    .detail-btn{
        width: 100%;
        margin: 0 auto;
        display: flow;
    }

    .detail-btn div {
        width: 160px;
        height: 50px;
        line-height: 14px;
        padding: 18px 0;
        font-size: 16px;
        box-sizing: border-box;
        background: #009966;
        color: #fff;
        text-align: center;
        margin-right: 15px;
        cursor: pointer;
        border-radius: 20px;
    }


    .headerBg{
        background-color: white !important;
    }

</style>