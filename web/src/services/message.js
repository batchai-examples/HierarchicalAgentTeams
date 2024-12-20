import { POST, GET } from './request'

export function newPost(content) {
  return POST('/posts', {
    content: content
  })
}

export function listAllPosts() {
  return GET('/posts')
}

export function newComment(parentId, content) {
  return POST(`/comments`, {
    parentId: parentId,
    content: content
  })
}
