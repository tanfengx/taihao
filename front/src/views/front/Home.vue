<script setup>
import {reactive, ref} from "vue";
import request from "@/utils/request";
import router from "@/router"


const name = ref('')
const state = reactive({
    noticeList:[],
        rotationList:[],
})


state.userOptions = []
request.get('/user').then(res => state.userOptions = res.data)

const pageNum = ref(1)
const pageSize = ref(5)
const total = ref(0)
const load = () => {

  //请求前面10条的公告
  request.get('/notice/findTop10').then(res => {
    state.noticeList = res.data
  })
}
load()  // 调用 load方法拿到后台数据

//轮播图
request.get('/front/banner/list').then(res => {
  state.rotationList = res.data
  state.rotationList = state.rotationList.filter((item) => item.indexRadio === '是');
})

//加载首页数据列表
request.get('/front/goods/page', {
  params: {
    pageNum: 1,
    pageSize: 8,
  }
}).then(res => {
  state.goodsData = res.data.records
})
request.get('/front/notice/page', {
  params: {
    pageNum: 1,
    pageSize: 8,
  }
}).then(res => {
  state.noticeData = res.data.records
})
const truncatedContent = (content,len) => {
    const maxLength = len;
    if (content.length > maxLength) {
        return content.substring(0, maxLength) + '...';
    }
    return content;
}

//推荐商品
request.get('/front/goods/recom').then(res => {
  state.recomData = res.data
})
</script>

<template>
  <div>
    <!-- 轮播图 -->
    <div style="margin-top: 10px;">
      <div style="width: 80%;margin: 0 auto;">
        <el-carousel :interval="5000" arrow="always" height="400px">
          <el-carousel-item v-for="item in state.rotationList" :key="item" v-show="item.indexRadio=='是'">
            <a :href="item.url" target="_blank"><img :src="item.img" alt="" style="width: 100%; height: 100%"></a>
          </el-carousel-item>
        </el-carousel>
      </div>
    </div>

    <div style="width:80%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 10px ;padding-top: 5px ;margin-top: 20px;">
          <span style="font-weight: bold; font-size: 22px;">推荐自行车</span>
        </div>
        <div>
          <el-row :gutter="10">
            <el-col :span="6" v-for="item in state.recomData" :key="item.id" style="margin-top: 20px;">
                <div ><img @click="router.push('/front/goods-detail?id=' + item.id)" :src="item.img" alt="" style="width: 100%; height: 240px;cursor: pointer;border-radius: 5px 5px 0px 0px;"></div>
                <div><span style="font-weight: bold;font-size: 16px;">{{ item.name}}</span></div>
                <div>
                  <span style="color:red;font-size: 18px;font-weight: bold;" v-if="item.price">￥{{item.price}}</span>
                </div>
            </el-col>
          </el-row>
        </div>
    </div>

      <div style="width:80%;margin: 0 auto;margin-bottom: 50px;">
        <div style="padding-bottom: 10px ;padding-top: 5px ;margin-top: 20px;">
          <span style="font-weight: bold; font-size: 22px;">自行车产品</span>
        </div>
        <div>
          <el-row :gutter="10">
            <el-col :span="6" v-for="item in state.goodsData" :key="item.id" style="margin-top: 20px;">
                <div ><img @click="router.push('/front/goods-detail?id=' + item.id)" :src="item.img" alt="" style="width: 100%; height: 240px;cursor: pointer;border-radius: 5px 5px 0px 0px;"></div>
                <div><span style="font-weight: bold;font-size: 16px;">{{ item.name}}</span></div>
                <div>
                  <span style="color:red;font-size: 18px;font-weight: bold;" v-if="item.price">￥{{item.price}}</span>
                </div>
            </el-col>
          </el-row>
        </div>
    </div>







        <div style="width:80%;margin: 0 auto;margin-bottom: 50px;">
            <div style="padding-bottom: 10px ;padding-top: 5px ;margin-top: 20px;">
                <span style="font-weight: bold; font-size: 22px;">平台公告</span>
            </div>
            <div>
                <div class="item" v-for="(item,index) in state.noticeData" :key="index" style="padding: 10px 0;">
                    <div class="right-container-data">
                        <div class="top">
                            <div class="rank-number">{{ index + 1 }}</div>
                            <div style="cursor: pointer;width:80%; "><a href="javascript:void(0)" class="title" @click="router.push('/front/notice-detail?id=' + item.id)">{{ item.name }}</a></div>
                            <!-- （可选）显示价格 -->
                            <div style="color: #fa5741;width:20%; " v-if="item.price">{{ item.price }} 元</div>
                        </div>
                        <div style="color: #6d6d73;font-weight: bold; font-size: 14px;height: 60px;overflow: hidden;" v-html="truncatedContent(item.content,300)"></div>
                        <div class="time">发布时间：{{ item.createTime }}</div>
                    </div>
                </div>
            </div>
        </div>

  </div>
</template>

<style scoped>
.refresh:hover {
  cursor: pointer;
}
:deep(.el-card__body) {
  padding: 10px !important;
}


/* 标题样式 */
.title {
  font-size: 18px;
  color: #333;  /* 标题默认颜色 */
  text-decoration: none;  /* 移除下划线 */
  /* 悬停效果 */
  transition: color 0.3s ease;
}

.title:hover {
  color: orangered !important;  /* 鼠标悬停时的颜色 */
}


.item {
  padding: 10px 0;
  display: flex;
  border-radius: 10px;
}

.item img {
  width: 160px;
  height: 120px;
}

.right-container {
  position: relative;
  margin-left: 20px;
  width: 100%;

}

.right-container div {
  margin-bottom: 7px;
}

.top {
  display: flex;
  color: #101d37;
  font-size: 20px;
  font-weight: bold;
  line-height: 25px;
}

.time {
  color: rgba(16, 29, 55, .3);
  font-size: 14px;
}

.right-container-data {
    position: relative;
    width: 100%;

}

.right-container-data div {
    margin-bottom: 7px;
}

.rank-number {
    font-size: 14px;
    font-weight: bold;
    margin-right: 10px;
    width: 25px;
    height: 25px;
    border-radius: 50%;
    background-color: #888888;
    color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
