<script setup>
import { RouterView } from 'vue-router'
import router from "@/router";
import {useUserStore} from "@/stores/user";
import request from "@/utils/request";
import {ElMessage} from "element-plus";
const userStore = useUserStore()
let user = userStore.getUser
const activePath = router.currentRoute.value.path.replace('/', '')

const logout = () => {
  request.get('/logout/' + user.uid).then(res => {
    if (res.code === '200') {
      userStore.logout()
    } else {
      ElMessage.error(res.msg)
    }
  })
}
const menus = userStore.getMenus

const getAvatarHandler = (avatar) => {
  user.avatar = avatar
}
</script>

<template>
  <div>

    <div style="display: flex;">
      <div class="manager-main-left">
        <el-menu
            :default-active="activePath"
            class="el-menu-demo"
            style="border: none"
            router
        >
        <div v-for="item in menus" :key="item.id">
          <div v-if="item.type === 2">
            <el-menu-item :index="item.path" v-if="!item.hide">
              <el-icon v-if="item.icon">
                <component :is="item.icon"></component>
              </el-icon>
              <span>{{ item.name }}</span>
            </el-menu-item>
          </div>
          <div v-else>
            <el-sub-menu :index="item.id + ''" v-if="!item.hide">
              <template #title>
                <el-icon v-if="item.icon">
                  <component :is="item.icon"></component>
                </el-icon>
                <span>{{ item.name }}</span>
              </template>
              <div  v-for="subItem in item.children" :key="subItem.id">
                <el-menu-item :index="subItem.path" v-if="!subItem.hide">
                  <template #title>
                    <el-icon v-if="subItem.icon">
                      <component :is="subItem.icon"></component>
                    </el-icon>
                    <span>{{ subItem.name }}</span>
                  </template>
                </el-menu-item>
              </div>
            </el-sub-menu>
          </div>
        </div>
        </el-menu>
      </div>

      <div style="flex: 1;">
        <div class="manager-header">
          <div style="display: flex">
            <div style="flex:1.2; color: #fff; font-weight: bold;  text-align: right; font-size: 20px;line-height: 60px;">
              在线销售自行车网站
            </div>

            <div style="flex: 1;">
              <div>
              </div>
              <div style="text-align: right; padding-right: 20px;line-height: 60px;">
                <el-dropdown>
                  <el-avatar :size="40" :src="user.avatar" style="margin-top: 10px" />
                  <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item><div @click="router.push('/front')">访问前台</div></el-dropdown-item>
                      <el-dropdown-item><div @click="router.push('/person')">个人信息</div></el-dropdown-item>
                      <el-dropdown-item><div @click="router.push('/password')">修改密码</div></el-dropdown-item>
                      <el-dropdown-item><div @click="logout">退出登录</div></el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
                <span style="margin-right: 5px; color: #FFFFFF">{{ user.name }}</span>
              </div>
            </div>
          </div>
        </div>
        <div style="padding: 10px;background-color: #f3f6fe;">
        <router-view v-slot="{ Component }">
          <component @getAvatar="getAvatarHandler" ref="childRef" :is="Component" />
        </router-view>
        </div>
      </div>
    </div>

  </div>
</template>
<style scoped>
  @import "@/assets/css/layout.css";
</style>
