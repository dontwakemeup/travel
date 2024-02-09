import openai
import streamlit as st
import config

st.title("趣味旅行")
client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "chat_started" not in st.session_state:
    st.session_state["chat_started"] = False
prompt_placeholder = st.empty()
if "preliminary_form_submitted" not in st.session_state:
    st.session_state["preliminary_form_submitted"] = False

if not st.session_state["preliminary_form_submitted"]:
    with st.form(key='preliminary_form'):
        st.session_state["budget"] = st.text_input('你的旅游费用预算是')
        st.session_state["number_of_people"] = st.text_input('出行人数')
        st.session_state["number_of_days"] = st.text_input('旅游天数')
        if st.form_submit_button(label='提交'):
            st.session_state["preliminary_form_submitted"] = True
# 问卷封面部分
if st.session_state["preliminary_form_submitted"]:
    if "form_selected" not in st.session_state:
        st.session_state["form_selected"] = None
        prompt_placeholder.markdown("请选择你的旅行者身份开启副本")
    cover_placeholder = st.empty()  # 创建一个新的占位符用于放置问卷封面按钮
    # 创建一个新的占位符用于显示提示信息
    if st.session_state["form_selected"] is None:
        cols = cover_placeholder.columns(3)  # 将问卷封面按钮放在新的占位符中
        with cols[0]:
            if st.button("问卷甲"):
                st.session_state["form_selected"] = "form1"
                st.session_state["chat_started"] = True
        with cols[1]:
            if st.button("问卷乙"):
                st.session_state["form_selected"] = "form2"
                st.session_state["chat_started"] = True
        with cols[2]:
            if st.button("问卷丙"):
                st.session_state["form_selected"] = "form3"
                st.session_state["chat_started"] = True
        if st.session_state["form_selected"] is not None:
            cover_placeholder.empty()  # 清空问卷封面按钮
            prompt_placeholder.empty()  # 清空提示信息
# 问卷部分
    if st.session_state["form_selected"] is not None:
        form_placeholder = st.empty()
        skip_button_placeholder = st.empty()  # 创建一个新的占位符用于放置跳过按钮

        if st.session_state["form_selected"] == "form1":
            if "option1" not in st.session_state:
                st.session_state["option1"] = ""
            if "option2" not in st.session_state:
                st.session_state["option2"] = ""
            if "option3" not in st.session_state:
                st.session_state["option3"] = ""
            if "option4" not in st.session_state:
                st.session_state["option4"] = ""
            if "option5" not in st.session_state:
                st.session_state["option5"] = ""

            option1 = st.radio(
                '您会选择以下哪种小众场景？',
                ('美食刺客，越刺越勇', '本地人都不知道的“世外桃源”', '打卡绝美拍照点，争做网红创始人',
                 '其他场景(请填写)')
            )
            st.session_state["option1"] = option1
            if st.session_state["option1"] == '其他场景(请填写)':
                st.session_state["option1"] = st.text_input('请填写你的答案', key='11')

            option2 = st.radio(
                '您的旅游必备单品是？',
                ('相机', '墨镜', '手电筒', '各种速食食品', '其他(请填写)')
            )
            st.session_state["option2"] = option2
            if st.session_state["option2"] == '其他(请填写)':
                st.session_state["option2"] = st.text_input('请填写你的答案', key='option2_key')

            option3 = st.radio(
                '抵达目的地后，以下哪种情景会影响您的心情？',
                ('景点没看头', '找不到好吃的餐馆', '手机突然没电', '其他(请填写)')
            )
            if st.session_state["option3"] == '其他(请填写)':
                st.session_state["option3"] = st.text_input('请填写你的答案', key='option3_key')
            else:
                st.session_state["option3"] = option3

            option4 = st.radio(
                '对您来说，本次旅途的目的是',
                ('逃离城市，探索自然', '促进感情，交换真心', '探索未知，自由惬意', '其他(请填写)')
            )
            st.session_state["option4"] = option4

            if st.session_state["option4"] == '其他(请填写)':

                st.session_state["option4"] = st.text_input('请填写你的答案', key='14')
            else:
                st.session_state["option4"] = option4
            option5 = st.radio(
                '旅途结束以后，您会选择',
                ('朋友圈分享本次旅程', '记录旅行VLOG', '编撰《XX的旅游日志》', '其他(请填写)')
            )
            if st.session_state["option5"] == '其他(请填写)':
                st.session_state["option5"] = st.text_input('请填写你的答案', key='option5_key')
            else:
                st.session_state["option5"] = option5
        if "form_submitted" not in st.session_state or not st.session_state["form_submitted"]:
            with form_placeholder.form(key='my_form'):
                    submit_button = st.form_submit_button(label='提交')
            skip_button = skip_button_placeholder.button('填问卷太麻烦？一键开启盲盒旅行')
            # 如果用户提交了问卷，将问卷结果作为聊天机器人的输入
            if submit_button or skip_button:
                st.session_state["form_submitted"] = True
                form_placeholder.empty()  # 清除问卷
                skip_button_placeholder.empty()  # 清除跳过按钮
                st.markdown("欢迎咨询旅游服务")  # 显示欢迎消息
                status_message = st.empty()  # 创建状态消息的占位符
                status_message.write("正在为您生成旅游计划...")  # 显示状态消息
                full_response = ""
                if submit_button:
                    status_message = st.empty()  # 创建状态消息的占位符
                    status_message.write("正在为您生成旅游计划...")  # 显示状态消息
                    full_response = ""
                    if st.session_state["form_selected"] == "form1":
                        input_text = f"请根据我给出的提示给我推荐一个适合我的旅游的地方，并且给我制定详细的计划：我的旅游预算是{st.session_state['budget']}，出行人数是{st.session_state['number_of_people']}，旅游天数是{st.session_state['number_of_days']}，在旅游时我更喜欢{st.session_state['option1']}，我的旅游必备单品是{st.session_state['option2']}，到达目的地之后我的心情会因为{st.session_state['option3']}而变差，我的旅游目的主要是{st.session_state['option4']}，在结束我的旅途后我喜欢 {st.session_state['option5']}"
                        st.write(input_text)  # 显示用户的输入
                    elif st.session_state["form_selected"] == "form2":
                        input_text = f"我选择了：我希望在{option1}之类的地方旅游，并且我喜欢以{option2}的方式观光，我喜欢{option3}之类的旅游项目，我希望我晚上在{option4}休息。"
                    else:
                        input_text = f"我选择了：我希望我旅游的时候可以躺在 {option1}，我喜欢{option2}之类的旅游项目，我希望我晚上在{option3}休息，通常我喜欢以{option4}的方式纪念我的旅途"
                elif skip_button:
                    # 当点击"填问卷太麻烦？一键开启盲盒旅行"按钮时，使用预备问卷的结果
                    input_text = f"给我安排一个详细的旅游计划：我的预算是 {st.session_state['budget']}，一共有{st.session_state['number_of_people']}人，打算玩{st.session_state['number_of_days']}天"
                for response in client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[{"role": "user", "content": input_text}],
                        stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                status_message.empty()  # 清除状态消息
                st.session_state.messages.append({"role": "assistant", "content": full_response})

# 在使用messages之前，检查它是否已经在session_state中初始化
if "messages" not in st.session_state:
    st.session_state["messages"] = []
# 聊天部分
if "form_submitted" in st.session_state and st.session_state["form_submitted"]:
    # 添加重置按钮
    if st.button('重置'):
        st.session_state.clear()
        st.experimental_rerun()  # 重定向到一个新的页面
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
        for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.get("messages", [])],
                stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
