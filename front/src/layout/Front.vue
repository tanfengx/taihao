<script setup>
import { RouterView } from 'vue-router'
import router from "@/router";
import {useUserStore} from "@/stores/user";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import {nextTick, ref} from "vue";
import config from "../../config";

const userStore = useUserStore()
let user = userStore.getUser
const activePath = router.currentRoute.value.path
const name = ref('')
name.value = router.currentRoute.value.query.name || ''
const childRef = ref()
const menus = ref([])


const logout = () => {
  request.get('/logout/' + user.uid).then(res => {
    if (res.code === '200') {
      userStore.logout()
	  window.location.href="/front"
    } else {
      ElMessage.error(res.msg)
    }
  })
}


const getAvatarHandler = (avatar) => {
  user.avatar = avatar
}

const search = () => {
  router.push('/front/goods?name=' + name.value)
}


</script>

<template>
  <div>
    <div style="width:80%;height: 60px; line-height: 60px;text-align: right;">
      <div style="font-size: 16px; color: #009966;" v-if="user.id">
        <el-avatar :size="30" :src="user.avatar" style="vertical-align: middle;" />
        {{ user.name }}
        <a href="javascript:void(0)" @click="router.push('/front/person')" class="loginCls">修改个人资料</a>
        <a href="javascript:void(0)" @click="router.push('/front/password')" class="loginCls">重置密码</a>
        <a href="javascript:void(0)" @click="logout" class="loginCls">退出登录</a>
      </div>
      <div style="flex: 3; font-size: 16px; color: #009966; margin-left: 180px;" v-else>
        <a href="javascript:void(0)" @click="router.push('/login')" class="loginCls">登录</a>
        <a href="javascript:void(0)" @click="router.push('/register-member')" class="loginCls">用户注册</a>
        <a href="javascript:void(0)" @click="router.push('/register-business')" class="loginCls">商家注册</a>
      </div>
    </div>

    <div style="height: 60px; line-height: 60px;box-shadow: rgba(0, 0, 0, 0.08) 0px 2px 4px 0px;">
      <div style="width:80%;margin: 0 auto;display: flex;">
      <div style="flex: 1;">
        <div style="font-size: 24px; color: #009966; font-weight: bold">{{config.projectName}}</div>
      </div>
      <div style="flex: 1.7;">
        <el-menu :default-active="activePath" mode="horizontal" router style="border: none; height: 100%; width: 100%;">
          <el-menu-item index="/front/home">首页</el-menu-item>
          <el-menu-item index="/front/notice">平台公告</el-menu-item>
          <el-menu-item index="/front/goods">浏览自行车</el-menu-item>
          <el-menu-item index="/front/cart">购物车</el-menu-item>
          <el-dropdown>
            <el-menu-item>个人中心</el-menu-item>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item><div @click="router.push('/front/address')">收货地址管理</div></el-dropdown-item>
                <el-dropdown-item><div @click="router.push('/front/orders')">我的商品订单</div></el-dropdown-item>
                <el-dropdown-item><div @click="router.push('/front/collect')">我的收藏</div></el-dropdown-item>
                <el-dropdown-item><div @click="router.push('/front/myservices')">我的售后服务</div></el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-menu>
      </div>
      <div style="flex: 1;">
        <!-- 搜索条 -->
          <el-input style="width: 250px" placeholder="搜索自行车" v-model="name" clearable size="large"></el-input>
          <el-button type="info" style="margin-left: 5px;" @click="search">搜索</el-button>
      </div>
      </div>
    </div>

    <div style="width: 100%; margin: 0 auto;min-height: 600px;">
      <router-view v-slot="{ Component }">
        <component @getAvatar="getAvatarHandler" @getUnread="getUnRead" ref="childRef" :is="Component" />
      </router-view>
    </div>


    <div style="height: 100px; line-height: 100px; border-top: 1px solid rgba(208,208,208,0.08);text-align: center;">
      <span>{{config.projectName}}@Copyright版权所有</span>
    </div>
  </div>
</template>

<style scoped>
  .badge {
    margin-top: 10px;
    margin-right: 40px;
  }
  :deep(.el-badge__content.is-fixed) {
    top: 10px !important;
  }

  .loginCls{
    margin-left: 25px;
    text-decoration: none;
    color: #009966;
  }
  .loginCls a {
    text-decoration: none;
    color: #333;
    transition: color 0.3s;
  }

  .loginCls:hover {
    color: #f00;
  }

  .loginCls:visited {
    color: #999;
  }

  .loginCls::after {
    content: '';
    width: 0;
    height: 1px;
    background-color: #f00;
    transition: width 0.3s;
  }

  .loginCls:hover::after {
    width: 100%;
  }
</style>
