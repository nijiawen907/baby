// 短信模板ID
const SMS_TEMPLATES = {
  ENVIRONMENT_ALERT: 'SMS_123456789', // 环境异常提醒
  DAILY_REPORT: 'SMS_987654321',     // 每日报告
  EMERGENCY: 'SMS_111222333'          // 紧急情况
}

// 订阅消息模板ID
const MESSAGE_TEMPLATES = {
  ENVIRONMENT_ALERT: 'MSG_123456789', // 环境异常提醒
  DAILY_REPORT: 'MSG_987654321',     // 每日报告
  EMERGENCY: 'MSG_111222333'         // 紧急情况
}

// 发送短信的API
export const sendSMS = async (phone, message, templateId = SMS_TEMPLATES.ENVIRONMENT_ALERT) => {
  try {
    // 验证手机号格式
    if (!/^1[3-9]\d{9}$/.test(phone)) {
      throw new Error('无效的手机号码')
    }

    // 这里替换为实际的短信API调用
    const response = await uni.request({
      url: 'your-sms-api-endpoint',
      method: 'POST',
      data: {
        phone,
        message,
        template_id: templateId,
        timestamp: Date.now()
      }
    })

    // 处理响应
    if (response.data.code === 0) {
      console.log('短信发送成功:', response.data)
      return response.data
    } else {
      throw new Error(response.data.message || '短信发送失败')
    }
  } catch (error) {
    console.error('发送短信失败:', error)
    // 可以在这里添加重试逻辑
    throw error
  }
}

// 发送小程序订阅消息
export const sendSubscribeMessage = async (templateId, data) => {
  try {
    // 获取订阅消息权限
    const {accept} = await uni.requestSubscribeMessage({
      tmplIds: [templateId]
    })
    
    if (accept) {
      // 发送订阅消息
      const response = await uni.request({
        url: 'your-subscribe-message-api-endpoint',
        method: 'POST',
        data: {
          template_id: templateId,
          ...data,
          page: 'pages/environment/environment', // 点击消息跳转的页面
          timestamp: Date.now()
        }
      })

      if (response.data.code === 0) {
        console.log('订阅消息发送成功:', response.data)
        return response.data
      } else {
        throw new Error(response.data.message || '订阅消息发送失败')
      }
    } else {
      throw new Error('用户未授权订阅消息')
    }
  } catch (error) {
    console.error('发送订阅消息失败:', error)
    throw error
  }
}

// 发送紧急预警
export const sendEmergencyAlert = async (data) => {
  try {
    // 同时发送短信和订阅消息
    await Promise.all([
      sendSMS(data.phone, data.message, SMS_TEMPLATES.EMERGENCY),
      sendSubscribeMessage(MESSAGE_TEMPLATES.EMERGENCY, {
        thing1: { value: '紧急预警' },
        thing2: { value: data.message },
        time3: { value: new Date().toLocaleString() }
      })
    ])

    // 可以添加其他紧急通知方式，如推送通知等
    return true
  } catch (error) {
    console.error('发送紧急预警失败:', error)
    throw error
  }
}

// 发送每日环境报告
export const sendDailyReport = async (phone, reportData) => {
  try {
    const message = formatDailyReport(reportData)
    await Promise.all([
      sendSMS(phone, message, SMS_TEMPLATES.DAILY_REPORT),
      sendSubscribeMessage(MESSAGE_TEMPLATES.DAILY_REPORT, {
        thing1: { value: '每日环境报告' },
        thing2: { value: message },
        time3: { value: new Date().toLocaleString() }
      })
    ])
    return true
  } catch (error) {
    console.error('发送每日报告失败:', error)
    throw error
  }
}

// 格式化每日报告
const formatDailyReport = (data) => {
  return `
今日环境报告:
温度: ${data.temperature}℃
湿度: ${data.humidity}%
舒适度: ${data.comfortScore}分
异常次数: ${data.alertCount}次
建议: ${data.suggestion}
  `.trim()
} 