import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_ENDPOINT,
  timeout: 2 * 1000,
  responseType: 'json',
  maxContentLength: 1024 * 1024,
  maxRedirects: 0,
  withCredentials: true // 允许跨域请求包含凭据
})

// request拦截器
service.interceptors.request.use(
  (config) => {
    // Do something before request is sent
    config.headers['Content-Type'] = 'application/json'

    // const sessionStore = useSessionStore()
    // const accessToken = sessionStore.session.token
    // if (accessToken) {
    //   // 让每个请求加上jwt token
    //   config.headers['Authorization'] = `Bearer ${accessToken}`
    // }

    return config
  },
  (error) => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// respone拦截器
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.log('err' + error) // for debug

    const errResp = error.response
    if (errResp && errResp.status === 401) {
      if (errResp.config.url.endsWith('/rest/signin')) {
        ElMessage.error('用户名或密码有误')
      } else {
        ElMessage.error('请登录')
      }
      // 重定向到登录页面
      //const router = useRouter()
      //router.push({ name: 'SignIn' })
    } else {
      ElMessage.error(error.message)
    }
    return Promise.reject(error)
  }
)

function POST(url, data) {
  const args = {
    method: 'post',
    url: '/rest' + url,
    data: data,
    headers: { 'Content-Type': 'application/json' }
  }
  return service(args)
}

function GET(url) {
  const args = {
    method: 'get',
    url: '/rest' + url,
    headers: { 'Content-Type': 'application/json' }
  }
  return service(args)
}

export { POST, GET }
