<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onBeforeUnmount, onMounted, reactive, ref, shallowRef,nextTick} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // 引入 css
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
  import config from "../../../config";

  const userStore = useUserStore()
  const user = userStore.getUser
  const pageNum = ref(1)
  const pageSize = ref(5)
  const total = ref(0)

  //判断用户是否登录
  if(user.id==null){
    router.push('/login')
  }

  let token = null;
  let auths = null;
  if(user.id!=null){
      token = userStore.getBearerToken
      auths =  userStore.getAuths
  }

  const valueHtml = ref('')  // 富文本内容
  // 编辑器实例，必须用 shallowRef
  const editorRef = shallowRef()
  const editorConfig = {
    placeholder: '请输入内容...',
    MENU_CONF: {
      uploadImage: {
        fieldName: 'file',
        server: `http://${config.serverUrl}/file/uploadImg`,
        headers: {
          Authorization: token
        }
      }
    }
  }

  const content = ref('')
  const viewShow = ref(false)
  const view = (value) => {
    viewShow.value = true
    content.value = value
  }
  const handleCreated = (editor) => {
    editorRef.value = editor // 记录 editor 实例，重要！
  }
  // 组件销毁时，也及时销毁编辑器
  onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
  })

  const rules = reactive({
    name: [
      { required: true, message: '请输入名称', trigger: 'blur' },
    ]
  })
  const ruleFormRef = ref()

  const dialogFormVisible = ref(false)
  const id = router.currentRoute.value.query.id
  let name = router.currentRoute.value.query.name

  const state = reactive({
    tableData: [],
    form: {}
  })

  state.searchKey = ''
  const load = () => {
    if(state.searchKey!=null && state.searchKey!=''){
      name = state.searchKey
    }
    request.get('/front/services/mypage', {
      params: {
        name: name,
        pageNum: pageNum.value,
        pageSize: pageSize.value,
      }
    }).then(res => {
      state.tableData = res.data.records
      total.value = res.data.total
    })
  }
  load()  // 调用 load方法拿到后台数据

  state.ordersOptions = []
  request.get('/front/orders/list').then(res => state.ordersOptions = res.data)
  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)

  // 新增
  const handleAdd = () => {
    dialogFormVisible.value = true
    nextTick(() => {
      ruleFormRef.value.resetFields()
      state.form = {}
      valueHtml.value = ''  // 富文本
    })
  }

  // 编辑
  const handleEdit = (raw) => {
    dialogFormVisible.value = true
    nextTick(() => {
      ruleFormRef.value.resetFields()
      state.form = JSON.parse(JSON.stringify(raw))
      valueHtml.value = raw.content  // 富文本
    })
  }

  // 保存
  const save = () => {
    ruleFormRef.value.validate(valid => {   // valid就是校验的结果
      if (valid) {
        state.form.content = valueHtml.value  // 富文本保存内容
        request.request({
          url: '/services',
          method: state.form.id ? 'put' : 'post',
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

  // 删除
  const del = (id) => {
    request.delete('/services/' + id).then(res => {
      if (res.code === '200') {
        ElMessage.success('操作成功')
        load()  // 刷新表格数据
      } else {
        ElMessage.error(res.msg)
      }
    })
  }

  const handleFileUploadSuccess = (res) => {
    state.form.file = res.data
    ElMessage.success('上传成功')
  }
  const handleImgUploadSuccess = (res) => {
    state.form.img = res.data
    ElMessage.success('上传成功')
  }
</script>

<template>
  <div>

    <div style="width: 80%;margin: 10px auto">
       <div style="padding-bottom: 15px ;margin-top: 20px;text-align: left;">
        <span style="font-size: 14px;margin-right: 20px;">首页 > 我的售后服务</span>
       </div>


        <div style="margin: 10px 0;text-align: right;">
          <el-button type="success" @click="handleAdd">
            <el-icon style="vertical-align: middle">
              <Plus />
            </el-icon>  <span style="vertical-align: middle"> 申请售后服务 </span>
          </el-button>
        </div>

        <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" :header-cell-class-name="'headerBg'">
          <el-table-column label="序号">
              <template #default="scope">
                  {{scope.$index+1}}
              </template>
          </el-table-column>
              <el-table-column label="售后订单"><template #default="scope"><span v-if="scope.row.orders_id">{{ state.ordersOptions.find(v => v.id === scope.row.orders_id) ? state.ordersOptions.find(v => v.id === scope.row.orders_id).name : '' }}</span></template></el-table-column>
              <el-table-column prop="type_radio" label="类型"></el-table-column>

              <el-table-column label="具体原因"><template #default="scope"><el-button @click="view(scope.row.content)">查看</el-button></template></el-table-column>
     
            
      <el-table-column prop="state_radio" label="状态"></el-table-column>
      <el-table-column prop="remarks" label="处理说明"></el-table-column>
            <el-table-column label="操作" width="220px;">
              <template #default="scope">
                <el-popconfirm title="您确定删除吗？" @confirm="del(scope.row.id)" v-if="scope.row.state_radio=='审核中'">
                  <template #reference>
                    <el-button type="danger" size="small">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
        </el-table>

        <div style="margin: 20px 0;">
          <el-pagination
                  @current-change="load"
                  @size-change="load"
                  v-model:current-page="pageNum"
                  v-model:page-size="pageSize"
                  background
                  :page-sizes="[4, 8, 12, 16]"
                  layout="total, prev, pager, next"
                  :total="total"
          />
        </div>


      <el-dialog v-model="viewShow" title="预览" width="40%">
        <div  id="editor-content-view" class="editor-content-view" v-html="content" style="padding: 0 20px"></div>
        <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewShow = false">关闭</el-button>
      </span>
        </template>
      </el-dialog>

      <el-dialog v-model="dialogFormVisible" title="申请售后服务" width="40%">
        <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="80px" style="padding: 0 20px" status-icon>
            <el-form-item prop="ordersId" label="售后订单">
          <el-select clearable v-model="state.form.orders_id" placeholder="请选择"  style="width: 100%">
            <el-option v-for="item in state.ordersOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="typeRadio" label="类型">
          <el-radio-group v-model="state.form.type_radio">
           <el-radio label="退货">退货</el-radio>
           <el-radio label="换货">换货</el-radio>
           <el-radio label="退款">退款</el-radio>
          </el-radio-group>        </el-form-item>

                  <el-form-item prop="content" label="具体原因">
          <div style="border: 1px solid #ccc">
    <Toolbar
        style="border-bottom: 1px solid #ccc"
        :editor="editorRef"
        :mode="'simple'"
    />
    <Editor
        style="height: 300px; overflow-y: hidden;"
        v-model="valueHtml"
        :defaultConfig="editorConfig"
        :mode="'simple'"
        @onCreated="handleCreated"
    />
  </div>        </el-form-item>
      
     
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
  </div>
</template>

<style scoped>
  .headerBg{
    background-color: white !important;
  }
</style>