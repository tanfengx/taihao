﻿<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {onMounted, reactive, ref} from "vue";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // 引入 css
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

  const userStore = useUserStore()
  const user = userStore.getUser
  const pageNum = ref(1)
  const pageSize = ref(5)
  const total = ref(0)

  
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

  state.searchKey = ''
  const load = () => {
    if(state.searchKey!=null && state.searchKey!=''){
      name = state.searchKey
    }
    request.get('/front/notice/page', {
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

  //轮播图
  request.get('/front/banner/list').then(res => {
    state.rotationList = res.data
    state.rotationList = state.rotationList.filter((item) => item.indexRadio === '否');
  })

  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)


  //搜索
  state.searchKey = ''
  const search = () =>{
    load()
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
          <span style="font-size: 14px;margin-right: 20px;">首页 > 平台公告</span>
        </div>

        <div style="padding-bottom: 15px ;text-align: left;">
          <div style="margin-top: 10px;">
            <el-input style="width: 200px" placeholder="查询平台公告" v-model="state.searchKey" clearable></el-input>
            <el-button type="info" style="margin-left: 5px" @click="search">查询</el-button>
          </div>
        </div>


        <el-table :data="state.tableData" style="width: 100%;margin-top: 20px;" :header-cell-class-name="'headerBg'">
          <el-table-column label="序号">
              <template #default="scope">
                  {{scope.$index+1}}
              </template>
          </el-table-column>
                <el-table-column label="内容"><template #default="scope"><el-button @click="view(scope.row.content)">查看</el-button></template></el-table-column>
      <el-table-column prop="name" label="名称"></el-table-column>
      <el-table-column label="创建人"><template #default="scope"><span v-if="scope.row.user_id">{{ state.userOptions.find(v => v.id === scope.row.user_id) ? state.userOptions.find(v => v.id === scope.row.user_id).name : '' }}</span></template></el-table-column>

                <el-table-column label="操作">
                        <template #default="scope"><el-button type="info" plain size="small" @click="router.push('/front/notice-detail?id='+scope.row.id)">浏览详情</el-button></template>
                </el-table-column>
        </el-table>

        <div class="page">
          <el-pagination
                  prev-text="上一页"
                  next-text="下一页"
                  @current-change="load"
                  @size-change="load"
                  v-model:current-page="pageNum"
                  v-model:page-size="pageSize"
                  :page-sizes="[4, 8, 12, 16]"
                  layout="prev, pager, next"
                  :total="total"
          />
        </div>

      <el-dialog v-model="viewShow" title="浏览内容" width="40%">
        <div  id="editor-content-view" class="editor-content-view" v-html="content" style="padding: 0 20px"></div>
        <template #footer>
      <span class="dialog-footer">
        <el-button @click="viewShow = false">关闭</el-button>
      </span>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<style>
  .navbar {
    background-color: #eeeeee;
    padding: 10px;
    justify-content: center;
  }

  .navbar a {
    font-size: 16px;
    color: #333;
    text-decoration: none;
    margin: 0 15px;
    padding: 5px;
    transition: color 0.3s;
  }

  .navbar a:hover {
    color: #ff6700;
  }

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

  .el-pagination .el-pager .number, .el-icon.more.el-icon-more {
    color: #656565 !important;
    border: 1px solid #EAEAEA;
    height: 34px !important;
    line-height: 34px !important;
    box-sizing: border-box;
  }

  .el-icon.more.btn-quicknext.el-icon-more {
    border-right: none;
  }

  .el-icon.more.btn-quickprev.el-icon-more {
    border-left: none;
  }

  .el-pagination .el-pager .number:not(:first-child) {
    border-right: none !important;
  }

  .el-pagination .el-pager .number.active {
    background: #FF9900;
    border: 1px solid #FF9900;
    color: #FFFFFF !important;
  }

  .headerBg{
      background-color: white !important;
  }
</style>