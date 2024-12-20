export function formatDateFromMilliseconds(milliseconds) {
  const date = new Date(milliseconds)

  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0') // 月份从0开始，因此加1，并且确保两位数
  const day = date.getDate().toString().padStart(2, '0') // 确保两位数

  const hours = date.getHours().toString().padStart(2, '0') // 确保两位数
  const minutes = date.getMinutes().toString().padStart(2, '0') // 确保两位数
  const seconds = date.getSeconds().toString().padStart(2, '0') // 确保两位数

  // 返回格式化的日期字符串
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}
