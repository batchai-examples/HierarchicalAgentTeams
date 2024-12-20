<template>
  <el-container style="justify-content: center; align-items: center">
    <el-card class="box-card" style="width: 400px">
      <template v-slot:header>
        <div class="clearfix">
          <span>注册</span>
        </div>
      </template>
      <el-form :model="signUpForm" :rules="rules" ref="signUpFormRef" label-width="120px">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="signUpForm.name"></el-input>
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="signUpForm.email"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="signUpForm.password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSignUp">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </el-container>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import * as sessionApi from '@/services/session'

const router = useRouter()

const signUpForm = reactive({
  name: '',
  password: '',
  email: ''
})

const rules = {
  name: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  email: [{ required: true, message: '请输入Email', trigger: 'blur' }]
}

const signUpFormRef = ref(null)

const handleSignUp = async () => {
  await signUpFormRef.value.validate(async (valid) => {
    if (valid) {
      await sessionApi.signUp(signUpForm.name, signUpForm.password, signUpForm.email)

      ElMessage.success('注册成功')

      router.push({ name: 'SignIn' })
    } else {
      ElMessage.error('请检查表单填写是否正确')
    }
  })
}
</script>

<style scoped>
.box-card {
  margin-top: 50px;
}
</style>
