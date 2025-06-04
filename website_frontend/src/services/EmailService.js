// src/services/EmailService.js
import axios from 'axios'

export function send_company_email(recipient, templateName, context) {
  return axios.post('/main/send-email/', {
    recipient,
    template_name: templateName,
    context
  })
}