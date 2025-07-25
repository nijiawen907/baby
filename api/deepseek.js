import OpenAI from "openai";

const openai = new OpenAI({
        baseURL: 'https://api.deepseek.com',
        apiKey: 'sk-2ffe9e008c9d425eb776f6a641faa45d',
		dangerouslyAllowBrowser: true
});

export async function getdeepseekapi(message) {
  try {
    const completion = await openai.chat.completions.create({
      messages: [
        { 
          role: "system", 
          content: "你是一个专业的婴儿护理助手,可以回答关于婴儿护理、健康、发育等方面的问题。" 
        },
        {
          role: "user",
          content: message
        }
      ],
      model: "deepseek-chat",
    });

    if (completion.choices && completion.choices[0] && completion.choices[0].message) {
      return completion.choices[0].message.content;
    } else {
      throw new Error('API返回格式错误');
    }
  } catch (error) {
    console.error('Deepseek API 调用失败:', error);
    throw error;
  }
}