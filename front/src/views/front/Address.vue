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
    request.get('/front/address/list').then(res => {
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

  //删除收货地址
  const deleteAddress =(id) =>{
      request.delete('/front/address/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('操作成功')
              load()  // 刷新表格数据
          } else {
              ElMessage.error(res.msg)
          }
      })
  }


  const name = ref('')
  const dialogFormVisible = ref(false)
  const rules = reactive({
      name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
      ]
  })
  const ruleFormRef = ref()
  // 编辑
  const handleEdit = (raw) => {
      dialogFormVisible.value = true
      nextTick(() => {
          ruleFormRef.value.resetFields()
          state.form = JSON.parse(JSON.stringify(raw))
      })
  }

  // 新增
  const handleAdd = () => {
      dialogFormVisible.value = true
      nextTick(() => {
          ruleFormRef.value.resetFields()
          state.form = {}
      })
  }

  // 保存
  const save = () => {
      ruleFormRef.value.validate(valid => {   // valid就是校验的结果
          if (valid) {
              state.form.userId = user.id
              state.form.defaultRadio='否'
              request.request({
                  url: '/front/address/update',
                  method: 'post',
                  data: state.form
              }).then(res => {
                  if (res.code === '200') {
                      ElMessage.success('保存成功')
                      dialogFormVisible.value = false
                      load()  // 刷新表格数据
                  } else {
                      ElMessage.error(res.msg)
                  }
              })
          }
      })
  }

  //设置默认收货地址
  const updateDefault =(id) =>{
      request.put('/front/address/setDefault/' + id).then(res => {
          if (res.code === '200') {
              ElMessage.success('操作成功')
              load()  // 刷新表格数据
          } else {
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
            <span style="font-size: 14px;margin-right: 20px;">首页 > 管理收货地址</span>
        </div>

         <div style="margin-top: 10px;text-align: right;">
            <el-button type="info" @click="handleAdd">新增收货地址</el-button>
         </div>

        <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" :header-cell-class-name="'headerBg'">
                <el-table-column prop="id" label="序号">
                  <template #default="scope">
                    {{ scope.$index + 1 }}
                  </template>
                </el-table-column>
                <el-table-column prop="name" label="姓名"></el-table-column>
                <el-table-column prop="phone" label="手机号码"></el-table-column>
                <el-table-column prop="address" label="详细地址"></el-table-column>
                <el-table-column prop="postcode" label="邮政编码"></el-table-column>
                <el-table-column prop="defaultRadio" label="是否默认"></el-table-column>
                <el-table-column label="操作" width="220px;">
                    <template #default="scope">
                        <el-button type="warning" size="small" @click="updateDefault(scope.row.id)" v-if="scope.row.defaultRadio=='否'">设为默认</el-button>
                        <el-button type="primary" size="small" @click="handleEdit(scope.row)">修改</el-button>
                        <el-button type="danger" size="small" @click="deleteAddress(scope.row.id)">删除</el-button>
                    </template>
                </el-table-column>
        </el-table>

    </div>

      <!-- 编辑收货地址 -->
      <el-dialog v-model="dialogFormVisible" title="收货地址信息" width="40%">
          <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="80px" style="padding: 0 20px" status-icon>
              <el-form-item prop="name" label="姓名">
                  <el-input v-model="state.form.name" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item prop="phone" label="手机号码">
                  <el-input v-model="state.form.phone" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item prop="address" label="详细地址">
                  <el-input v-model="state.form.address" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item prop="postcode" label="邮政编码">
                  <el-input v-model="state.form.postcode" autocomplete="off"></el-input>
              </el-form-item>

          </el-form>
          <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取消</el-button>
        <el-button type="primary" @click="save">
          保存
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