import { createRouter, createWebHistory } from 'vue-router'
import {useUserStore} from "@/stores/user"
const modules = import.meta.glob('../views/*.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Layout',
      redirect: '/home',
      component: () => import('../layout/Layout.vue'),
      children: [
        { path: 'home', name: 'Home', component: () => import('../views/Home.vue') },
        { path: 'person', name: 'Person', component: () => import('../views/Person.vue') },
        { path: 'password', name: 'Password', component: () => import('../views/Password.vue') },
      ]
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/Login.vue')
    },
	    {
      path: '/register-business',
      name: 'Register-business',
      component: () => import('../views/Register-business.vue')
    },
    {
      path: '/register-member',
      name: 'Register-member',
      component: () => import('../views/Register-member.vue')
    },
    {
      path: '/404',
      name: '404',
      component: () => import('../views/404.vue')
    },
	// 前台页面路由
    {
      path: '/front',
      name: 'Front',
      redirect: '/front/home',
      component: () => import('../layout/Front.vue'),
      children: [
        { path: 'home', name: 'FrontHome', component: () => import('../views/front/Home.vue') },
        { path: 'person', name: 'person', component: () => import('../views/front/Person.vue') },
        { path: 'password', name: 'password', component: () => import('../views/front/Password.vue') },
        { path: 'notice', name: 'notice', component: () => import('../views/front/Notice.vue') },
        { path: 'goods', name: 'goods', component: () => import('../views/front/Goods.vue') },
        { path: 'cart', name: 'cart', component: () => import('../views/front/Cart.vue') },
        { path: 'address', name: 'address', component: () => import('../views/front/Address.vue') },
        { path: 'orders', name: 'orders', component: () => import('../views/front/Orders.vue') },
        { path: 'collect', name: 'collect', component: () => import('../views/front/Collect.vue') },
        { path: 'services', name: 'services', component: () => import('../views/front/Services.vue') },
        { path: 'myservices', name: 'myservices', component: () => import('../views/front/myservices.vue') },
          { path: 'notice-detail', name: 'notice-detail', component: () => import('../views/front/NoticeDetail.vue') },
          { path: 'goods-detail', name: 'goods-detail', component: () => import('../views/front/GoodsDetail.vue') },
          { path: 'services-detail', name: 'services-detail', component: () => import('../views/front/ServicesDetail.vue') },
      ]
    }
  ]
})

// 注意：刷新页面会导致页面路由重置
export const setRoutes = (menus) => {
  if (!menus || !menus.length) {
    const manager = localStorage.getItem('manager')
    if (!manager) {
      return
    }
    menus = JSON.parse(manager).managerInfo.menus
  }

  if (menus.length) {
    // 开始渲染 未来的不确定的  用户添加的路由
    menus.forEach(item => {   // 所有的页面都需要设置路由，而目录不需要设置路由
      if (item.path) {  // 当且仅当path不为空的时候才去设置路由
        router.addRoute('Layout', { path: item.path, name: item.page, component: modules['../views/' + item.page + '.vue'] })
      } else {
        if (item.children && item.children.length) {
          item.children.forEach(sub => {
            if (sub.path) {
              router.addRoute('Layout', { path: sub.path, name: sub.page, component: modules['../views/' + sub.page + '.vue'] })
            }
          })
        }
      }
    })
  }
}

setRoutes()


// 路由守卫
router.beforeEach((to, from, next) => {
  if (!to.matched.length) {
    next('/404')
  } else {
    next()
  }
})

export default router
