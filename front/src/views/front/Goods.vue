<script setup>
  import {nextTick, onBeforeUnmount, reactive, ref, shallowRef} from "vue";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import {useUserStore} from "@/stores/user";
  import router from "@/router"
  import config from "../../../config";

  const userStore = useUserStore()
  const user = userStore.getUser

  
  const pageNum = ref(1)
  const pageSize = ref(8)
  const total = ref(0)

  let name = router.currentRoute.value.query.name
  const state = reactive({
    tableData: [],
  })

  state.searchKey = ''
  const load = (key) => {
    if(state.searchKey!=null && state.searchKey!=''){
      name = state.searchKey
    }
    request.get('/front/goods/page', {
      params: {
        name: name,
        pageNum: pageNum.value,
        pageSize: pageSize.value,
        category_id:state.category_id,
      }
    }).then(res => {
      state.tableData = res.data.records
      total.value = res.data.total
    })
  }
  load()

  //轮播图
  request.get('/front/banner/list').then(res => {
    state.rotationList = res.data
    state.rotationList = state.rotationList.filter((item) => item.indexRadio === '否');
  })

  state.categoryOptions = []
  request.get('/front/category/list').then(res => state.categoryOptions = res.data)
  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)

  state.category_id = ''
  const getCategory = (category_id) =>{
    state.category_id = category_id
    if(category_id=='all'){
      state.category_id = ''
    }
    load()
  }

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
          <span style="font-size: 14px;margin-right: 20px;">首页 > 浏览自行车</span>
        </div>

      <div style="display:flex;">
        <div style="padding-bottom: 15px ;margin-top: 20px;text-align: left;line-height: 30px;flex: 1;margin-right: 10px;">
          <div style="margin-right: 10px;" class="categorybar">
            <a href="javascript:void(0)" @click="getCategory('all')">全部</a>
          </div>
          <div v-for="item in state.categoryOptions" :key="item.id" style="margin-right: 10px;border-top: 1px solid #ffffff;" class="categorybar">
            <a href="javascript:void(0)" @click="getCategory(item.id)">{{item.name}}</a>
          </div>
        </div>

        <div style="flex: 5;">
            <div style="margin-top: 10px;">
                <el-input style="width: 200px" placeholder="请输入关键词" v-model="state.searchKey" clearable></el-input>
                <el-button type="info" style="margin-left: 5px" @click="search" >查询</el-button>
            </div>
            <div>
              <el-row :gutter="10">
                <el-col :span="6" v-for="item in state.tableData" :key="item.id" style="margin-top: 20px;">
                    <div ><img @click="router.push('/front/goods-detail?id=' + item.id)" :src="item.img" alt="" style="width: 95%; height: 200px;cursor: pointer;border-radius: 5px 5px 0px 0px;"></div>
                    <div><span style="font-size: 16px;">{{ item.name}}</span></div>
                    <div>
                        <span style="color:red;font-size: 18px;font-weight: bold;" v-if="item.price">￥{{item.price}}</span>
                    </div>
                </el-col>
              </el-row>
            </div>

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
        </div>
      </div>
    </div>

  </div>
</template>
<style>
   .categorybar {
    padding: 10px;
    justify-content: center;
    border-radius: 10px;
    margin-top: 10px;
    text-align: center;
   }

   .categorybar:hover {
       background-color: #efefef;
   }

  .categorybar a {
   font-size: 16px;
   color: #666;
   text-decoration: none;
   margin: 0 15px;
   padding: 5px;
   transition: color 0.3s;
   font-weight: bold;
  }

  .categorybar a:hover {
    color: #009966;
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

</style>