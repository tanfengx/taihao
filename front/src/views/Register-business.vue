<script setup>
import { reactive, ref} from "vue"
import { User, Lock, Message } from '@element-plus/icons-vue'
import request from "@/utils/request";
import {ElMessage} from "element-plus";
import router from "@/router";
import config from "../../config";

  const loginData = reactive({})
  const rules = reactive({
    username: [
      { required: true, message: '请输入登录账号', trigger: 'blur' },
    ],
    email: [
      { required: true, message: '请输入邮箱', trigger: 'blur' },
      { type: 'email', message: '请输入正确的邮箱格式', trigger: ['blur', 'change'] }
    ],
    password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 3, max: 20, message: '密码长度在3-20位之间', trigger: 'blur' },
    ],
    confirmPassword: [
      { required: true, message: '请确认密码', trigger: 'blur' },
      { min: 3, max: 20, message: '密码长度在3-20位之间', trigger: 'blur' },
    ],
  })
  const ruleFormRef = ref()
  const register = () => {
    ruleFormRef.value.validate(valid => {
      if (valid) {
        if (loginData.password !== loginData.confirmPassword) {
          ElMessage.warning('两次密码不一致')
          return;
        }
		loginData.role = 'business'
        // 发送表单数据给后台
        request.post('/register', loginData).then(res => {
          if (res.code === '200') {
            ElMessage.success('注册成功')
            router.push('/login')
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
    })
  }

</script>

<template>
  <div class="wrapper">
    <div style="width: 100%; background-color: #009966;padding: 15px 30px; color: white; font-size: 40px;text-align:center;">{{config.projectName}}</div>
    <div style="margin: 40px auto; background-color: #fff; width: 500px; height: 500px; padding: 20px;border-radius: 10px;box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.3);">
      <div style="margin: 20px 0; text-align: center; font-size: 24px;color: #333;"><b>商家注册</b></div>
      <el-form
              ref="ruleFormRef"
              :model="loginData"
              :rules="rules"
              size="large"
              status-icon
      >
        <el-form-item prop="username">
          <el-input v-model="loginData.username" placeholder="请输入登录账号"  />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="loginData.email" placeholder="请输入邮箱"  />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginData.password" show-password placeholder="请输入密码" />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="loginData.confirmPassword" show-password placeholder="请确认密码"/>
        </el-form-item>
        <el-form-item style="margin: 10px 0; text-align: right">
          <el-button type="primary" autocomplete="off" @click="register">确认注册</el-button>
          <el-button autocomplete="off" @click="router.push('/login')">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
        <div style="text-align: center;">
          <a style="text-decoration: none; color: #333;margin-left: 20px;" href="/front/home">访问前台系统</a>
        </div>
    </div>
  </div>
</template>
<style>
  .wrapper {
    background-image: url("../assets/6004f52a56ccb1610937642123.jpg");
    background-repeat: no-repeat;
    background-size: cover;
    height: 100vh;
    overflow: hidden;
  }
</style>
