<!-- 主页面组件，包含登录/登出按钮、新留言按钮、留言和评论树的显示逻辑，以及新留言和新评论对话框的实现 -->
<template>
  <div style="margin-top: 50px">
    <div v-if="sessionStore.authenticated">
      当前用户：{{ sessionStore.session.user.name + ' (' + sessionStore.session.user.email + ')' }}
    </div>
    <br />
    <el-button @click="refreshMessages">刷新</el-button>
    <el-button @click="toggleSignIn">{{ sessionStore.authenticated ? '退出' : '登录' }}</el-button>
    <RouterLink to="/signup">注册</RouterLink>
    <el-button @click="openNewPostDialog" v-if="sessionStore.authenticated">发表新留言</el-button>
    <br /><br /><br />
    <div class="custom-tree-container" style="margin-bottom: 20px">
      <el-tree
        style="max-width: 600px"
        :data="messages"
        :props="{ children: 'replies', label: 'content' }"
        node-key="id"
        default-expand-all
        :expand-on-click-node="false"
      >
        <template #default="{ node, data }">
          <span class="tree-node">
            <span>{{ node.label }}</span>
            <span>{{ data.createdBy }} ({{ formatDateFromMilliseconds(data.createdAt) }})</span>
            <span>
              <a @click="replyToComment(data)" v-if="sessionStore.authenticated"> 回复 </a>
            </span>
          </span>
        </template>
      </el-tree>
    </div>

    <!-- 发表新留言对话框 -->
    <el-dialog v-model="newPostDialogVisible" title="发表新留言" width="800">
      <el-form :model="newPostForm" @submit.prevent="submitNewPost">
        <el-form-item label="内容" :error="newPostError">
          <el-input
            type="textarea"
            v-model="newPostForm.content"
            maxlength="200"
            show-word-limit
            @input="checkNewPostLength"
          ></el-input>
          <span>{{ newPostLength }}</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitNewPost">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 发表新评论对话框 -->
    <el-dialog v-model="newCommentDialogVisible" title="发表新评论" width="800">
      <el-form :model="newCommentForm" @submit.prevent="submitNewComment">
        <el-form-item label="内容" :error="newCommentError">
          <el-input
            type="textarea"
            v-model="newCommentForm.content"
            maxlength="200"
            show-word-limit
            @input="checkNewCommentLength"
          ></el-input>
          <span>{{ newCommentLength }}</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitNewComment">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'
import * as messageApi from '@/services/message'
import { formatDateFromMilliseconds } from '@/utils/date'

const router = useRouter()
const sessionStore = useSessionStore()

const messages = ref([])

const newPostDialogVisible = ref(false)
const newPostForm = ref({ content: '' })
const newPostError = ref('')
const newPostLength = ref('')

const newCommentDialogVisible = ref(false)
const newCommentForm = ref({ content: '', parentId: '' })
const newCommentError = ref('')
const newCommentLength = ref('')
const currentMessage = ref(null)

// 登录状态切换
const toggleSignIn = () => {
  if (sessionStore.authenticated) {
    sessionStore.signOut()
  } else {
    router.push({ name: 'SignIn' })
  }
}

// 显示新留言对话框
const openNewPostDialog = () => {
  newPostDialogVisible.value = true
}

// 新留言长度校验
const checkNewPostLength = () => {
  const length = newPostForm.value.content.length
  newPostLength.value = `还可以输入 ${200 - length} 字`
  newPostError.value = length < 3 ? '留言长度需在3~200字之间' : ''
}

// 提交新留言（进行长度校验）
const submitNewPost = async () => {
  if (newPostForm.value.content.length < 3 || newPostForm.value.content.length > 200) {
    newPostError.value = '留言长度需在3~200字之间'
    return
  }

  newPostDialogVisible.value = false

  const newPost = await messageApi.newPost(newPostForm.value.content)
  messages.value.unshift(newPost)
  refreshMessages()

  newPostForm.value.content = ''
  newPostLength.value = ''
}

// 回复评论（打开新评论对话框，并记录当前评论对象）
const replyToComment = (node) => {
  currentMessage.value = node
  newCommentDialogVisible.value = true
}

// 新评论长度校验（动态提示还可以输入多少字）
const checkNewCommentLength = () => {
  const length = newCommentForm.value.content.length
  newCommentLength.value = `还可以输入 ${200 - length} 字`
  newCommentError.value = length < 3 ? '评论长度需在3~200字之间' : ''
}

// 提交新评论（进行长度校验）
const submitNewComment = async () => {
  if (newCommentForm.value.content.length < 3 || newCommentForm.value.content.length > 200) {
    newCommentError.value = '评论长度需在3~200字之间'
    return
  }

  newCommentDialogVisible.value = false

  const parentId = currentMessage.value.id
  /*const newComment = */ await messageApi.newComment(parentId, newCommentForm.value.content)
  //currentMessage.value.replies.unshift(newComment);
  await refreshMessages()

  newCommentForm.value.content = ''
  newCommentLength.value = ''
}

const refreshMessages = async () => {
  messages.value = await messageApi.listAllPosts()
}

onMounted(async () => {
  await refreshMessages()
})
</script>

<style scoped>
.tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>
