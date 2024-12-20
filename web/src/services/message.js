import { POST } from './request'

export function ping(msg) {
  return POST('/ping', {msg})
}
