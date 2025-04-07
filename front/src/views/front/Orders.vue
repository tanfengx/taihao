<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onMounted, reactive, ref, nextTick} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // 引入 css
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

  const userStore = useUserStore()
  const user = userStore.getUser
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

  const state = reactive({
    tableData:[],
    form:{},
  })

  const load = () => {
    request.get('/front/orders/list').then(res => {
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

  //删除订单
  const deleteOrders =(id) =>{
      request.delete('/front/orders/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('操作成功')
              load()  // 刷新表格数据
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  //取消订单
  const cancelOrders =(id) =>{
      request.put('/front/orders/cancel/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('操作成功')
              load()  // 刷新表格数据
          } else {
              ElMessage.error(res.msg)
          }
      })
  }

  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)

  //弹出评论
  state.goodids = ''
  const dialogFormVisible = ref(false)
  const handlerCommentAdd = (id,goodids,bizUserId) =>{
      dialogFormVisible.value = true
      state.goodids = goodids
      state.form.ordersId = id
      state.form.bizUserId = bizUserId
  }
  //保存评价
  state.orders = {}
  const saveComment = () => {
      let array = state.goodids.split(',')
      array.forEach((e,i)=> {
          state.form.goodsId = e  // 当前模块的id
          state.form.userId = user.id //用户id
          // 发送数据
          request.post('/front/comments/update', state.form).then(res => {
              if (res.code === '200') {
                  dialogFormVisible.value = false
              } else {
                  ElMessage.error(res.msg)
                  return
              }
          })
      });
      //修改订单状态为'已评价'
      state.orders.id = state.form.ordersId
      state.orders.stateRadio = '已评价'
      request.post('/front/orders/update',state.orders).then(res => {
          if (res.code === '200') {
              load()  // 刷新表格数据
          } else {
              ElMessage.error(res.msg)
          }
      })
      ElMessage.success("评论成功")
  }

    //确认收货
    const handlerConfirm = (id) =>{
    let orders = {}
	orders.id = id
	orders.stateRadio='已收货'
	request.post('/front/orders/update',orders,{dataType: 'json'}).then(res => {
		if(res.code=='200'){
			load()  // 刷新表格数据
		}else{
			ElMessage.error(res.msg)
        }
	})
  }

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
            <span style="font-size: 14px;margin-right: 20px;">首页 > 我的订单</span>
        </div>

          <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" :header-cell-class-name="'headerBg'">
                <el-table-column prop="id" label="序号">
                  <template #default="scope">
                    {{ scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column prop="name" label="订单号"></el-table-column>
                <el-table-column label="商户" width="250px;">
                    <template #default="scope">
                        <span v-if="scope.row.bizUserId">{{ state.userOptions.find(v => v.id === scope.row.bizUserId) ? state.userOptions.find(v => v.id === scope.row.bizUserId).name : '' }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="订单明细"><template #default="scope"><el-button @click="view(scope.row.content)">查看</el-button></template></el-table-column>
                <el-table-column prop="amount" label="订单总金额"></el-table-column>
              <el-table-column prop="createTime" label="下单时间"></el-table-column>
                <el-table-column prop="stateRadio" label="订单状态"></el-table-column>
              <el-table-column label="操作" width="200px;">
                  <template #default="scope">
                      <el-button type="danger" size="small" @click="deleteOrders(scope.row.id)" v-if="scope.row.stateRadio=='已下单'">删除</el-button>
                      <el-button type="warning" size="small" @click="cancelOrders(scope.row.id)" v-if="scope.row.stateRadio=='已下单'">取消</el-button>
                      <el-button type="primary" size="small" @click="handlerConfirm(scope.row.id)" v-if="scope.row.stateRadio=='已发货'">确认收货</el-button>
                      <el-button type="primary" size="small" @click="handlerCommentAdd(scope.row.id,scope.row.goodids,scope.row.bizUserId)" v-if="scope.row.stateRadio=='已收货'">评价</el-button>
                  </template>
              </el-table-column>
        </el-table>

    </div>

      <el-dialog v-model="viewShow" title="预览" width="40%">
          <div  id="editor-content-view" class="editor-content-view" v-html="content" style="padding: 0 20px"></div>
          <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewShow = false">关闭</el-button>
      </span>
          </template>
      </el-dialog>

          <!-- 评论窗口 -->
          <el-dialog v-model="dialogFormVisible" title="评论" width="30%">
              <el-form :model="state.form" label-width="50px" style="padding: 0 20px" status-icon>
                  <el-form-item label="评分">
                      <el-rate v-model="state.form.score">
                      </el-rate>
                  </el-form-item>
                  <el-form-item label="内容">
                      <el-input type="textarea" :rows="5" v-model="state.form.content" autocomplete="off"></el-input>
                  </el-form-item>
              </el-form>
              <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="saveComment">
          确定
        </el-button>
      </span>
              </template>
          </el-dialog>
  </div>
</template>

<style>
.headerBg{
    background-color: white !important;
}
</style>