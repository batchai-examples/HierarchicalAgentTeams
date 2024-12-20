import { POST } from './request'

export function signUp(name, password, email) {
  return POST('/signup', { name, password, email })
}

export function signIn(name, password) {
  return POST('/signin', { name, password })
}
