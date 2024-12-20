import { createRouter, createWebHistory } from 'vue-router'
import MessageBoard from '../views/qa.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MessageBoard',
      component: MessageBoard
    }
  ]
})

export default router
