﻿<script setup>
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


  const id = router.currentRoute.value.query.id // 参数id
  const state = reactive({
    data: {},
  })

  const load = () => {
    request.get('/front/goods/' + id).then(res => {
      state.data = res.data
    })

  }
  onMounted(() => {
    load()
  })

  //轮播图
  request.get('/front/banner/list').then(res => {
    state.rotationList = res.data
    state.rotationList = state.rotationList.filter((item) => item.indexRadio === '否');
  })

  //购物车
  state.num = 1;
  //添加购物车
  const addCart = () =>{
    //判断用户是否登录
    if(user.id==null){
      router.push('/login')
      return
    }

    if(state.data.userId!=null && state.data.userId==user.id){
      ElMessage.error('不能添加自己的商品')
      return
    }

    //加入购物车
    request.request({
      url: '/front/cart/update',
      method: 'post',
      data: {
        userId:user.id,
        name:state.data.name,
        img:state.data.img,
        num:state.num,
        price:state.data.price,
        bizUserId:state.data.userId,
        goodid:state.data.id,
      }
    }).then(res => {
      if (res.code === '200') {
        ElMessage.success('添加成功')
        router.push('/front/cart')
      } else {
        ElMessage.error(res.msg)
      }
    })

  }

  state.activeTab = 'content'

  //加载评论
  const loadComments = () =>{
    request.get('/front/comments/tree?goodsId=' + id).then(res => {
      state.comments = res.data
    })
  }
  loadComments();

  const dialogFormVisible = ref(false)
  //弹出评论框
  const handleComment = (row) => {
    //判断是否登录
    if(user.id==null){
      ElMessage.error('请先登录')
      return
    }
    dialogFormVisible.value = true
    state.form = {}
    if (row && row.id) {  // row是父节点的数据，如果存在，则为评论
      state.parent = row
    }
  }

  //保存评论
  state.parent = {}
  const save = () => {
    if (state.parent.id) {  // 回复的时候触发
      state.form.pid = state.parent.id
      state.form.puserId = state.parent.user.id  // 传父级评论的用户id
    }
    state.form.goodsId = id  // 当前模块的id
    state.form.userId = user.id //用户id
    // 发送数据
    request.post('/front/comments/update', state.form).then(res => {
      if (res.code === '200') {
        ElMessage.success("评论成功")
        dialogFormVisible.value = false
        loadComments()
        state.parent = {}
      } else {
        ElMessage.error(res.msg)
      }
    })
  }

  //删除评论
  const del = (id) => {
    request.delete('/front/comments/' + id).then(res => {
      if (res.code === '200') {
        ElMessage.success("删除成功")
        loadComments()
      } else {
        ElMessage.error(res.msg)
      }
    })
  }

  state.categoryOptions = []
  request.get('/front/category/list').then(res => state.categoryOptions = res.data)
  state.userOptions = []
  request.get('/front/user/list').then(res => state.userOptions = res.data)

  state.collect = {}
  state.collectStatus = false
  //查询自行车收藏状态
  const checkCollect = () =>{
    if(user.id==null){
      state.collectStatus = false
      return
    }
    request.get('/front/collect/collect/'+id+'/'+user.id).then(res => {
      state.collectStatus = res.data
    })
  }
  checkCollect()
  //添加自行车收藏
  const addCollect = () =>{
    //判断是否登录
    if(user.id==null){
      ElMessage.error('请先登录')
      return
    }
    state.collect.userId = user.id
    state.collect.goodsId = id
    request.post('/front/collect/update', state.collect).then(res => {
      if (res.code === '200') {
        ElMessage.success("收藏成功")
        checkCollect()
      } else {
        ElMessage.error(res.msg)
      }
    })
  }
  //取消自行车收藏
  const deleteCollect = () =>{
    //判断是否登录
    if(user.id==null){
      ElMessage.error('请先登录')
      return
    }
    request.delete('/front/collect/' + id +'/'+user.id).then(res => {
      if (res.code === '200') {
        ElMessage.success("取消收藏成功")
        checkCollect()
      } else {
        ElMessage.error(res.msg)
      }
    })
  }

  //增加浏览量
  const updateGoodsViews = () =>{
    request.post('/front/goods/views/update/'+id).then(res => {})
  }
  updateGoodsViews()

</script>

<template>
  <div>

    <div class="mc detail-container">
        <div style="padding-bottom: 15px ;text-align: left;">
          <span style="font-size: 14px;margin-right: 20px;">首页 > {{ state.data.name }}</span>
        </div>

        <div class="detail-content">
          <div class="detail-left">
            <img :src="state.data.img" style="height: 400px;width: 100%;border-radius: 10px 10px 0px 0px;"/>
          </div>
          <div class="detail-right">
            <div class="big-name"> {{ state.data.name }}</div>
            <div class="detail-info-list">
              <div>
                <span>商品分类：</span>{{ state.categoryOptions.find(v => v.id === state.data.categoryId) ? state.categoryOptions.find(v => v.id === state.data.categoryId).name : '' }}
              </div>
              <div>
                <span>价格：</span><span style="color: red;font-size: 20px;;">￥{{ state.data.price }}</span>
              </div>
              <div>
                <span>发布商家：</span>{{ state.userOptions.find(v => v.id === state.data.userId) ? state.userOptions.find(v => v.id === state.data.userId).name : '' }}
              </div>
              <div>
                <span>发布时间：</span>{{ state.data.createTime }}
              </div>
              <div>
                <span>浏览量：</span>{{ state.data.views }}
              </div>
            </div>
            <div style="margin-top: 20px;">
              <el-input-number
                      v-model="state.num"
                      :min="1"
                      :max="100"
                      label="数量"/>
            </div>
            <div class="detail-btn" style="margin-top: 20px">
                <el-button type="primary" @click="addCart" size="large">加入购物车</el-button>
                <el-button type="success" plain @click="addCollect" v-if="!state.collectStatus" size="large">收藏</el-button>
                <el-button type="info" @click="deleteCollect" v-if="state.collectStatus" size="large">取消收藏</el-button>
            </div>

          </div>
        </div>


        <el-tabs v-model="state.activeTab" style="margin-top: 20px;min-height: 500px;">
          <el-tab-pane label="图文详情" name="content">
            <span class="markdown-body" v-html="state.data.content"></span>
          </el-tab-pane>
          <el-tab-pane label="用户评价" name="comments">
            <div v-if="state.comments && state.comments.length">
              <div v-for="item in state.comments" :key="item.id" style="padding: 10px 20px;">
                <div style="display: flex; align-items: center">
                  <img v-if="item.user" style="width: 40px; height: 40px; border-radius: 50%"  :src="item.user.avatar" alt="">
                  <span v-if="item.user" style="margin-left: 10px; font-weight: bold">{{ item.user.name }}<el-rate v-model="item.score" style="margin-left: 10px;" :disabled="true"></el-rate></span>
                </div>

                <div style="line-height: 30px; padding-left: 50px; color: #666; margin: 5px 0">{{ item.content }}</div>

                <div style="padding-left: 50px; font-size: 12px; color: #999; display: flex">
                  <div style="flex: 1">
                    <el-icon style="top: 2px"><Clock /></el-icon> <span>{{item.createTime }}</span>
                  </div>

                  <div style="flex: 1; text-align: right">
                    <el-button type="danger" link style="color: red;" v-if="item.userId === user.id"  @click="del(item.id)">删除</el-button>
                  </div>
                </div>

                <div style="margin-top: 20px; margin-left: 50px; border-bottom: 1px solid #ddd;">
                  <!-- 回复的子节点 -->
                  <div v-for="subItem in item.children" :key="subItem.id" style="padding: 10px 0">
                    <div style="display: flex; align-items: center">
                      <img v-if="subItem.user" style="width: 40px; height: 40px; border-radius: 50%"  :src="subItem.user.avatar" alt="">
                      <span v-if="subItem.user" style="margin-left: 10px; font-weight: bold">{{ subItem.user.name }}</span>
                    </div>

                    <div style="line-height: 30px; padding-left: 50px; color: #666; margin: 5px 0">
                      <span style="color: #999">回复<span style="color: orange" v-if="subItem.puser">@{{ subItem.puser.name }}</span></span>
                      <span style="margin-left: 10px">{{ subItem.content }}</span>
                    </div>

                    <div style="padding-left: 50px; font-size: 12px; color: #999; display: flex">
                      <div style="flex: 1">
                        <el-icon style="top: 2px"><Clock /></el-icon> <span>{{subItem.createTime }}</span>
                      </div>

                      <div style="flex: 1; text-align: right">
                        <el-button type="danger" link style="color: red;" @click="del(subItem.id)" v-if="subItem.userId === user.id">删除</el-button>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>

            <div v-else style="margin: 10px 0; color: #999">
              暂时还没有评论哦！
            </div>

          </el-tab-pane>
        </el-tabs>

    </div>

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
        <el-button type="primary" @click="save">
          确定
        </el-button>
      </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
  .detail-container {
    padding: 20px 0;
    width:80%;margin: 0 auto;margin-bottom: 50px;
  }

  .big-name {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    font-size: 20px;
    line-height: 40px;
    color: #101d37;
  }


  .detail-content {
    display: flex;
  }

  .detail-left {
    width: 40%;
    margin-right: 2%;
  }

  .detail-right {
    width: 58%;
    box-sizing: border-box;
    height: 400px;
  }

  .detail-tag div {
    background-color: rgba(132, 154, 174, .1);
    border-radius: 2px;
    display: inline-block;
    padding: 2px 10px;
    height: 23px;
    line-height: 23px;
    text-align: center;
    font-size: 12px;
    color: #849aae;
    margin-right: 5px;
    margin-bottom: 5px;
  }

  .detail-info-list {
    padding: 10px 0;
    border-bottom: 1px solid #e4e6f0;
  }

  .detail-info-list div {
    margin-bottom: 5px;
    font-size: 14px;
  }

  .detail-info-list div span {
    color: #9399a5;

  }

  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
  }

  .detail-btn {
    display: flex;

  }

</style>