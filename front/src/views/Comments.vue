<script setup>
import router from "@/router";
import { nextTick, reactive, ref } from "vue";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import config from "../../config";
import {useUserStore} from "@/stores/user";
import { onBeforeUnmount, shallowRef} from "vue" 
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'


const name = ref('')
const pageNum = ref(1)
const pageSize = ref(10)
const total = ref(0)

const userStore = useUserStore()
const token = userStore.getBearerToken
const auths =  userStore.getAuths
const user = userStore.getUser

const state = reactive({
  tableData: [],
  form: {}
})

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
state.bizUserOptions = []
request.get('/user').then(res => state.bizUserOptions = res.data)
state.goodsOptions = []
request.get('/goods').then(res => state.goodsOptions = res.data)
state.ordersOptions = []
request.get('/orders').then(res => state.ordersOptions = res.data)
state.puserOptions = []
request.get('/puser').then(res => state.puserOptions = res.data)
state.userOptions = []
request.get('/user').then(res => state.userOptions = res.data)


const multipleSelection = ref([])

// 批量删除
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}

const confirmDelBatch = () => {
  if (!multipleSelection.value || !multipleSelection.value.length) {
    ElMessage.warning("请选择数据")
    return
  }
  const idArr = multipleSelection.value.map(v => v.id)
  request.post('/comments/del/batch', idArr).then(res => {
    if (res.code === '200') {
      ElMessage.success('操作成功')
      load()  // 刷新表格数据
    } else {
      ElMessage.error(res.msg)
    }
  })
}

const load = () => {
  request.get('/comments/page', {
    params: {
      name: name.value,
      pageNum: pageNum.value,
      pageSize: pageSize.value
    }
  }).then(res => {
    state.tableData = res.data.records
    total.value = res.data.total
  })
}
load()  // 调用 load方法拿到后台数据

const reset = () => {
  name.value = ''
  load()
}

const dialogFormVisible = ref(false)

const rules = reactive({
  name: [
    { required: true, message: '请输入名称', trigger: 'blur' },
  ]
})
const ruleFormRef = ref()

// 新增
const handleAdd = () => {
  dialogFormVisible.value = true
  nextTick(() => {
    ruleFormRef.value.resetFields()
    state.form = {}
    valueHtml.value = ''  // 富文本
  })
}

// 保存
const save = () => {
  ruleFormRef.value.validate(valid => {   // valid就是校验的结果
    if (valid) {
      state.form.content = valueHtml.value  // 富文本保存内容
      request.request({
        url: '/comments',
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

// 编辑
const handleEdit = (raw) => {
  dialogFormVisible.value = true
  nextTick(() => {
    ruleFormRef.value.resetFields()
    state.form = JSON.parse(JSON.stringify(raw))
    valueHtml.value = raw.content  // 富文本
  })
}

// 删除
const del = (id) => {
  request.delete('/comments/' + id).then(res => {
    if (res.code === '200') {
      ElMessage.success('操作成功')
      load()  // 刷新表格数据
    } else {
      ElMessage.error(res.msg)
    }
  })
}

// 导出接口
const exportData = () => {
  window.open(`http://${config.serverUrl}/comments/export`)
}


const handleImportSuccess = () => {
  // 刷新表格
  load()
  ElMessage.success("导入成功")
}

const handleFileUploadSuccess = (res) => {
  state.form.file = res.data
  ElMessage.success('上传成功')
}
const handleImgUploadSuccess = (res) => {
  state.form.img = res.data
  ElMessage.success('上传成功')
}

//弹出评论框
const dialogCommentsFormVisible = ref(false)
const handleComment = (row) => {
  //判断是否登录
  if(user.id==null){
    ElMessage.error('请先登录')
    return
  }
  dialogCommentsFormVisible.value = true
  state.form = {}
  if (row && row.id) {  // row是父节点的数据，如果存在，则为评论
    state.parent = row
    //alert(JSON.stringify(state.parent))
  }
  state.form.goodsId = row.goodsId
}

state.parent = {}
const saveComment = () => {
  if (state.parent.id) {  // 回复的时候触发
    state.form.pid = state.parent.id
    state.form.puserId = state.parent.userId  // 传父级评论的用户id
  }
  state.form.userId = user.id //用户id
  // 发送数据
  request.post('/front/comments/update', state.form).then(res => {
    if (res.code === '200') {
      ElMessage.success("回复评论成功")
      dialogCommentsFormVisible.value = false
      state.parent = {}
    } else {
      ElMessage.error(res.msg)
    }
  })
}
</script>

<template>
  <div>
    <div class="card" style="text-align: right;">
    
    </div>

    <div class="card"  style="text-align: right;">
    <div>
      <el-button type="success" @click="handleAdd" v-if="auths.includes('comments.add')">
        <el-icon style="vertical-align: middle">
          <Plus />
        </el-icon>  <span style="vertical-align: middle"> 添加 </span>
      </el-button>
      <el-upload
          v-if="auths.includes('comments.import')"
          class="ml5"
          :show-file-list="false"
          style="display: inline-block; position: relative; top: 3px"
          :action='`http://${config.serverUrl}/comments/import`'
          :on-success="handleImportSuccess"
          :headers="{ Authorization: token}"
      >
        <el-button type="primary">
          <el-icon style="vertical-align: middle">
            <Bottom />
          </el-icon>  <span style="vertical-align: middle"> 导入 </span>
        </el-button>
      </el-upload>
      <el-button type="primary" @click="exportData" class="ml5" v-if="auths.includes('comments.export')">
        <el-icon style="vertical-align: middle">
          <Top />
        </el-icon>  <span style="vertical-align: middle"> 导出 </span>
      </el-button>
      <el-popconfirm title="您确定删除吗？" @confirm="confirmDelBatch" v-if="auths.includes('comments.deleteBatch')">
        <template #reference>
          <el-button type="danger" style="margin-left: 5px">
            <el-icon style="vertical-align: middle">
              <Remove />
            </el-icon>  <span style="vertical-align: middle"> 批量删除 </span>
          </el-button>
        </template>
      </el-popconfirm>
    </div>
    </div>

    <div class="card">
    <div>
      <el-table :data="state.tableData" stripe  @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column label="序号">
           <template #default="scope">
             {{scope.$index+1}}
           </template>
         </el-table-column>
      <el-table-column label="商家编号"><template #default="scope"><span v-if="scope.row.biz_user_id">{{ state.bizUserOptions.find(v => v.id === scope.row.biz_user_id) ? state.bizUserOptions.find(v => v.id === scope.row.biz_user_id).name : '' }}</span></template></el-table-column>
      <el-table-column label="评论内容"><template #default="scope"><el-button @click="view(scope.row.content)">查看</el-button></template></el-table-column>
      <el-table-column label="商品编号"><template #default="scope"><span v-if="scope.row.goods_id">{{ state.goodsOptions.find(v => v.id === scope.row.goods_id) ? state.goodsOptions.find(v => v.id === scope.row.goods_id).name : '' }}</span></template></el-table-column>
      <el-table-column label="订单编号"><template #default="scope"><span v-if="scope.row.orders_id">{{ state.ordersOptions.find(v => v.id === scope.row.orders_id) ? state.ordersOptions.find(v => v.id === scope.row.orders_id).name : '' }}</span></template></el-table-column>
      <el-table-column prop="score" label="评论星级"></el-table-column>
      <el-table-column label="用户"><template #default="scope"><span v-if="scope.row.user_id">{{ state.userOptions.find(v => v.id === scope.row.user_id) ? state.userOptions.find(v => v.id === scope.row.user_id).name : '' }}</span></template></el-table-column>

        <el-table-column label="操作" width="220">
          <template #default="scope">
            <el-button type="success" @click="handleComment(scope.row)">回复评论</el-button>
            <el-button type="primary" size="small" @click="handleEdit(scope.row)" v-if="auths.includes('comments.edit')">修改</el-button>
            <el-popconfirm title="您确定删除吗？" @confirm="del(scope.row.id)" v-if="auths.includes('comments.delete')">
              <template #reference>
                <el-button type="danger" size="small">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="page">
      <el-pagination
          prev-text="上一页"
          next-text="下一页"
          @current-change="load"
          @size-change="load"
          v-model:current-page="pageNum"
          v-model:page-size="pageSize"
          background
          :page-sizes="[4, 8, 12, 16]"
          layout="prev, pager, next, total"
          :total="total"
      />
    </div>
    </div>

    <el-dialog v-model="dialogFormVisible" title="订单评论信息" width="40%">
      <el-form ref="ruleFormRef" :rules="rules" :model="state.form" label-width="80px" style="padding: 0 20px" status-icon>
        <el-form-item prop="content" label="评论内容">
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
        <el-form-item prop="goodsId" label="商品编号">
          <el-select clearable v-model="state.form.goods_id" placeholder="请选择"  style="width: 100%">
            <el-option v-for="item in state.goodsOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="ordersId" label="订单编号">
          <el-select clearable v-model="state.form.orders_id" placeholder="请选择"  style="width: 100%">
            <el-option v-for="item in state.ordersOptions" :key="item.id" :label="item.name" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item prop="pid" label="父评论ID">
          <el-input v-model="state.form.pid" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item prop="score" label="评论星级">
          <el-input v-model="state.form.score" autocomplete="off"></el-input>
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

    <el-dialog v-model="viewShow" title="预览" width="40%">
      <div  id="editor-content-view" class="editor-content-view" v-html="content" style="padding: 0 20px"></div>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewShow = false">关闭</el-button>
      </span>
      </template>
    </el-dialog>

    <el-dialog v-model="dialogCommentsFormVisible" title="回复评论" width="30%">
      <el-form :model="state.form" label-width="50px" style="padding: 0 20px" status-icon>
        <el-form-item label="内容">
          <el-input type="textarea" :rows="5" v-model="state.form.content" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogCommentsFormVisible = false">取消</el-button>
        <el-button type="primary" @click="saveComment">
          确定
        </el-button>
      </span>
      </template>
    </el-dialog>

  </div>
</template>
<style>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 13px;
  color: #656565;
  margin-top: 20px;
  padding-bottom: 20px;
}

.page > div.homePage, .page > div.lastPage {
  height: 34px;
  line-height: 34px;
  width: 60px;
  text-align: center;
  border: 1px solid #EAEAEA;
  box-sizing: border-box;
  cursor: pointer;
}

.page > div.homePage {
  border-radius: 2px 0 0 2px;
}

.page > div.lastPage {
  border-radius: 0 2px 2px 0;
}

.el-pagination {
  text-align: center;
  padding: 0;
}

.el-pagination > button {
  padding: 0 !important;
  height: 34px !important;
}

.el-pagination > button.btn-prev {
  border-right: none !important;
}

.el-pagination span {
  color: #656565;
  width: 50px;
  border: 1px solid #EAEAEA;
  height: 34px !important;
  line-height: 34px !important;
  box-sizing: border-box;
}

.card {
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 5px 0 rgba(0,0,0,.1);
  margin-top: 10px;
}
</style>