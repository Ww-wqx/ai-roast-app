import streamlit as st
from openai import OpenAI
import httpx

# ✅ DeepSeek API
client = OpenAI(
    api_key="sk-bf0ef7c363ad41589870da0539d4b09c", 
    base_url="https://api.deepseek.com",
    http_client=httpx.Client(trust_env=False, timeout=30)
)

st.title("🤖 AI吐槽机（智能配图版·免API）")

# 🎯 用关键词生成图片（无需API）
def get_image(keyword):
    # 用 Unsplash 关键词搜索
    return f"https://loremflickr.com/600/400/{keyword}"


# 👉 输入 + 回车提交
with st.form(key="roast_form"):
    user_input = st.text_input("请输入你想被吐槽的内容：")
    submit = st.form_submit_button("开始吐槽")


if submit:
    if user_input:

        # 🧠 AI生成：吐槽 + 英文关键词
        response = client.chat.completions.create(
            model="deepseek-chat",
            temperature=0.9,
            messages=[
                {
                    "role": "system",
                    "content": """
你是一个毒舌但幽默的吐槽大师，同时也是配图专家。

请你输出：
1）一段吐槽（中文，犀利幽默）
2）一个英文关键词（用于搜索图片，必须是简单词，比如 lazy / funny / awkward）

⚠️ 输出格式必须严格如下：

吐槽：xxxx
关键词：xxxx
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        result = response.choices[0].message.content

        # 🧩 解析结果
        try:
            roast_text = result.split("吐槽：")[1].split("关键词：")[0].strip()
            keyword = result.split("关键词：")[1].strip()
        except:
            roast_text = result
            keyword = "funny"

        # 🎯 获取图片
        img_url = get_image(keyword)

        # 🎬 展示
        st.write("😏 吐槽结果：")
        st.write(roast_text)

        st.image(img_url, caption=f"关键词：{keyword}")

    else:
        st.warning("请输入内容！")