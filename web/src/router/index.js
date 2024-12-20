import { createRouter, createWebHistory } from 'vue-router'
import QuestionAndAnswer from '../views/qa.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'qa',
      component: QuestionAndAnswer
    }
  ]
})

export default router
