<script setup>
import * as echarts from 'echarts'
import {onMounted, reactive} from "vue";
import request from "@/utils/request";

const state = reactive({
    categoryCount:'',
  goodsCount:'',
  ordersCount:'',
  commentsCount:'',
  form:{
    orderSalaryStartDate:null,
    orderSalaryEndDate:null,
  }
})

onMounted(() => {
  //获取数量
  request.get('/statistics/categoryCount').then(res => {
    state.categoryCount = res.data
  })
  request.get('/statistics/goodsCount').then(res => {
    state.goodsCount = res.data
  })
  request.get('/statistics/ordersCount').then(res => {
    state.ordersCount = res.data
  })
  request.get('/statistics/commentsCount').then(res => {
    state.commentsCount = res.data
  })

  load()

})

const load = () =>{

  let goodsCategoryOption = {
    title: {
      text: '商品分类数量统计',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)' // 添加此行以显示百分比
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: '50%',
        data: [],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  let chart_goodsCategory = echarts.init(document.getElementById("chart_goodsCategory"))
  request.get('/statistics/goodsCategory',{
    params:{
    }
  }).then(res => {
    if(res.data==null){
      chart_goodsCategory.setOption(goodsCategoryOption)
      return;
    }
    goodsCategoryOption.series[0].data = res.data
    // 绘制图表
    chart_goodsCategory.setOption(goodsCategoryOption)
  })







  let orderSalaryOption = {
    title: {
      text: '自行车销量统计图',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    xAxis: {
      type: 'category',
      data: []
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [],
        type: 'bar',
        itemStyle: {
          color: function() {
            var letters = "0123456789ABCDEF";
            var color = "#";
            for (var i = 0; i < 6; i++) {
              color += letters[Math.floor(Math.random() * 16)];
            }
            return color;
          }
        }
      }
    ]
  };
  let chart_orderSalary = echarts.init(document.getElementById("chart_orderSalary"))
  request.get('/statistics/orderSalary',{
    params:{
      beginDate:state.form.orderSalaryStartDate,
      endDate:state.form.orderSalaryEndDate,
    }
  }).then(res => {
    if(res.data==null){
      chart_orderSalary.setOption(orderSalaryOption)
      return;
    }
    orderSalaryOption.series[0].data = res.data.map(v => v.value)
    orderSalaryOption.xAxis.data = res.data.map(v => v.name)
    // 绘制图表
    chart_orderSalary.setOption(orderSalaryOption)
  })




}



const orderSalary_search = () =>{
  load();
}
const orderSalary_clear = () =>{
  state.form.orderSalaryStartDate=null
  state.form.orderSalaryEndDate=null
}


</script>

<template>
  <div style="background-color: #ffffff;padding: 10px;border-radius: 10px;margin-top: 20px;">
    <div>
      <el-row :gutter="10">

        <el-col :span="6">
          <el-card style="height: 100px;">
            <div style="color: #888">商品分类数量</div>
            <div style="font-size: 24px; font-weight: bold; text-align: center">{{ state.categoryCount.categoryCount }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card style="height: 100px;">
            <div style="color: #888">商品数量</div>
            <div style="font-size: 24px; font-weight: bold; text-align: center">{{ state.goodsCount.goodsCount }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card style="height: 100px;">
            <div style="color: #888">订单数量</div>
            <div style="font-size: 24px; font-weight: bold; text-align: center">{{ state.ordersCount.ordersCount }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card style="height: 100px;">
            <div style="color: #888">评价数量</div>
            <div style="font-size: 24px; font-weight: bold; text-align: center">{{ state.commentsCount.commentsCount }}</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div style="margin: 20px 0;">
      <el-row :gutter="10">

        <el-col :span="24">
          <div style="width:100%; height: 500px" id="chart_goodsCategory"></div>
        </el-col>
        <el-col :span="24">
          <div style="height: 80px;text-align: center;">
            从：<el-date-picker v-model="state.form.orderSalaryStartDate" type="date" value-format="YYYY-MM-DD" placeholder="开始时间" style="width:160px;"></el-date-picker>
            到：<el-date-picker v-model="state.form.orderSalaryEndDate" type="date" value-format="YYYY-MM-DD" placeholder="结束时间" style="width:160px;"></el-date-picker>
            <el-button style="margin-left: 5px" @click="orderSalary_search" type="primary" >查询</el-button>
            <el-button style="margin-left: 5px" @click="orderSalary_clear" type="warning" plain>清空</el-button>
          </div>
          <div style="width:100%; height: 500px" id="chart_orderSalary"></div>
        </el-col>
      </el-row>
    </div>


  </div>
</template>
