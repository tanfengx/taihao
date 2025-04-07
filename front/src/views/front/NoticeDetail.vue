<script setup>
  import router from "@/router";
  import request from "@/utils/request";
  import {onMounted, reactive, ref} from "vue";
  import {ElMessage} from "element-plus";
  import {useUserStore} from "@/stores/user";
  import '@wangeditor/editor/dist/css/style.css' // 引入 css
  import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

  const userStore = useUserStore()
  const user = userStore.getUser

  
  const id = router.currentRoute.value.query.id // 参数id
  const state = reactive({
    data: {},
  })

  const load = () => {
    request.get('/front/notice/' + id).then(res => {
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



</script>

<template>
  <div>

    <div style="width:80%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 15px ;margin-top: 20px;text-align: left;">
          <span style="font-size: 14px;margin-right: 20px;">首页 > {{ state.data.name }}</span>
        </div>

        <div style="padding-bottom: 15px ; margin-top: 20px;text-align: center;">
          <span style="font-size: 24px;">{{ state.data.name }}</span>
        </div>

        <div style="padding-bottom: 15px ; margin-top: 10px;text-align: center;">
                <span style="font-size: 14px;margin-right: 20px;">创建时间：{{ state.data.createTime }}</span>
        </div>


        <div class="editor-content-view" v-html="state.data.content" style="min-height: 200px;line-height: 30px;"></div>


    </div>

  </div>
</template>