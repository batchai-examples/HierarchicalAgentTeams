import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// TODO：改用accessToken + refreshToken

// 设置带过期时间的本地存储
function setItemWithExpiry(key, value, expiryInDays) {
  const now = new Date()
  const expiryTime = now.getTime() + expiryInDays * 24 * 60 * 60 * 1000
  const item = {
    value: value,
    expiry: expiryTime
  }
  localStorage.setItem(key, JSON.stringify(item))
}

// 获取带过期时间的本地存储
function getItemWithExpiry(key) {
  const itemStr = localStorage.getItem(key)
  if (!itemStr) {
    return null
  }
  const item = JSON.parse(itemStr)
  const now = new Date()
  // 检查项目是否已过期
  if (now.getTime() > item.expiry) {
    // 如果已过期，删除项目并返回null
    localStorage.removeItem(key)
    return null
  }
  return item.value
}

export const useSessionStore = defineStore('session', () => {
  const rememberedSession = getItemWithExpiry('session')
  const session = ref(
    rememberedSession
      ? rememberedSession
      : {
          token: '',
          user: {
            id: '',
            name: '',
            email: ''
          }
        }
  )

  const authenticated = computed(() => session.value.token && session.value.token.length > 0)

  function signOut() {
    session.value = {}
    localStorage.removeItem('session')
  }

  function signIn(newSession, rememberMe) {
    session.value = newSession
    if (rememberMe) {
      setItemWithExpiry('session', newSession, 30)
    }
  }

  return { session, authenticated, signOut, signIn }
})
