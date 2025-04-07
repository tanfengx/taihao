<script setup>
import {reactive} from "vue";
import request from "@/utils/request";
import dayjs from "dayjs";
import {useUserStore} from "@/stores/user";

const userStore = useUserStore()
const user = userStore.getUser

const state = reactive({
  notice: []
})

const load = () => {
  request.get("/notice").then(res => {
    state.notice = res.data
  })
}

const dateFliter = (val, format = "YYYY-MM-DD hh:mm:ss") => {
  if (!isNaN(val)) {
    val = parseInt(val);
  }
  return dayjs(val).format(format);
};
load()
</script>

<template>
  <div>
    <div class="card" style="padding: 15px">
      您好，{{ user?.name }}！欢迎使用本系统
    </div>

      <div class="card">
        <div style="margin-bottom: 30px; font-size: 20px; font-weight: bold">公告列表</div>
        <div >
          <el-timeline  reverse slot="reference">
            <el-timeline-item v-for="item in state.notice" :key="item.id" :timestamp="item.createTime">
              <el-popover
                      placement="right"
                      width="200"
                      trigger="hover"
                      :content="item.name">
                <template #reference>
                  {{ item.name }}
                </template>
              </el-popover>
            </el-timeline-item>
          </el-timeline>
        </div>
    </div>
  </div>
</template>
<style>
.card {
  padding: 20px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 2px 5px 0 rgba(0,0,0,.1);
  margin-top: 10px;
}
</style>
