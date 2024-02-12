import openai
import streamlit as st


st.title("趣味旅行")
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
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
        title = st.markdown("# 趣人格H5定制旅游测评")
        st.session_state["budget"] = st.text_input('你的旅游费用预算是（元）')
        st.session_state["number_of_people"] = st.text_input('出行人数（人）')
        st.session_state["number_of_days"] = st.text_input('旅游天数（天）')
        if st.form_submit_button(label='提交'):
            st.session_state["preliminary_form_submitted"] = True
            title.empty()
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
            if st.button("一身反骨的“景点刺客”"):
                st.session_state["form_selected"] = "form1"
                st.session_state["chat_started"] = True
        with cols[1]:
            if st.button("用脚步丈量大地的“背包客”"):
                st.session_state["form_selected"] = "form2"
                st.session_state["chat_started"] = True
        with cols[2]:
            if st.button("只想躺平的佛系现代人"):
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
            if "aoption1" not in st.session_state:
                st.session_state["aoption1"] = ""
            if "aoption2" not in st.session_state:
                st.session_state["aoption2"] = ""
            if "aoption3" not in st.session_state:
                st.session_state["aoption3"] = ""
            if "aoption4" not in st.session_state:
                st.session_state["aoption4"] = ""
            if "aption5" not in st.session_state:
                st.session_state["aoption5"] = ""

            aoption1 = st.radio(
                '您会选择以下哪种小众场景？',
                ('美食刺客，越刺越勇', '本地人都不知道的“世外桃源”', '打卡绝美拍照点，争做网红创始人',
                 '其他场景(请填写)')
            )
            st.session_state["aoption1"] = aoption1
            if st.session_state["aoption1"] == '其他场景(请填写)':
                st.session_state["aoption1"] = st.text_input('请填写你的答案', key='aoption1')

            aoption2 = st.radio(
                '您的旅游必备单品是？',
                ('相机', '墨镜', '手电筒', '各种速食食品', '其他(请填写)')
            )
            st.session_state["aoption2"] = aoption2
            if st.session_state["aoption2"] == '其他(请填写)':
                st.session_state["aoption2"] = st.text_input('请填写你的答案', key='aoption2_key')

            aoption3 = st.radio(
                '抵达目的地后，以下哪种情景会影响您的心情？',
                ('景点没看头', '找不到好吃的餐馆', '手机突然没电', '其他(请填写)')
            )
            st.session_state["aoption3"] = aoption3
            if st.session_state["aoption3"] == '其他(请填写)':
                st.session_state["aoption3"] = st.text_input('请填写你的答案', key='aoption3_key')

            aoption4 = st.radio(
                '对您来说，本次旅途的目的是',
                ('逃离城市，探索自然', '促进感情，交换真心', '探索未知，自由惬意', '其他(请填写)')
            )
            st.session_state["aoption4"] = aoption4

            if st.session_state["aoption4"] == '其他(请填写)':
                st.session_state["aoption4"] = st.text_input('请填写你的答案', key='aoption4_key')

            aoption5 = st.radio(
                '旅途结束以后，您会选择',
                ('朋友圈分享本次旅程', '记录旅行VLOG', '编撰《XX的旅游日志》', '其他(请填写)')
            )
            st.session_state["aoption5"] = aoption5
            if st.session_state["aoption5"] == '其他(请填写)':
                st.session_state["aoption5"] = st.text_input('请填写你的答案', key='1option5_key')

        elif st.session_state["form_selected"] == "form2":
            if "boption1" not in st.session_state:
                st.session_state["boption1"] = ""
            if "boption2" not in st.session_state:
                st.session_state["boption2"] = ""
            if "boption3" not in st.session_state:
                st.session_state["boption3"] = ""
            if "boption4" not in st.session_state:
                st.session_state["boption4"] = ""
            boption1 = st.radio(
                '请您选择降落位置',
                ('五岳', '青藏高原', '秦岭淮河一线', '甘肃沙漠', '岛屿孤勇者', '其他(请填写)')
            )
            st.session_state["boption1"] = boption1
            if st.session_state["boption1"] == '其他(请填写)':
                st.session_state["boption1"] = st.text_input('请填写你的答案', key='boption1_key')

            boption2 = st.radio(
                '请选择您的坐骑',
                ('越野车', '缆车', '观光大巴', '徒步最香', '其他(请填写)')
            )
            st.session_state["boption2"] = boption2
            if st.session_state["boption2"] == '其他(请填写)':
                st.session_state["boption2"] = st.text_input('请填写你的答案', key='boption2_key')

            boption3 = st.radio(
                '请选择挑战项目',
                ('极限运动', '山间野趣', '洞穴奇案', '勇闯“孤岛"', '其他(请填写)')
            )
            st.session_state["boption3"] = boption3
            if st.session_state["boption3"] == '其他(请填写)':
                st.session_state["boption3"] = st.text_input('请填写你的答案', key='boption3_key')

            boption4 = st.radio(
                '请选择您的驿站',
                ('帐篷', '房车', '青年旅社', '酒店', '其他(请填写)')
            )
            st.session_state["boption4"] = boption4
            if st.session_state["boption4"] == '其他(请填写)':
                st.session_state["boption4"] = st.text_input('请填写你的答案', key='boption4_key')


        else:
            if "coption1" not in st.session_state:
                st.session_state["coption1"] = ""
            if "coption2" not in st.session_state:
                st.session_state["coption2"] = ""
            if "coption3" not in st.session_state:
                st.session_state["coption3"] = ""
            if "coption4" not in st.session_state:
                st.session_state["coption4"] = ""
            coption1 = st.radio(
                '您偏好的躺平场景',
                ('观光度假村', '日落海滩', '主题民宿大床房', '农家乐', '其他(请填写)')
            )
            st.session_state["coption1"] = coption1
            if st.session_state["coption1"] == '其他(请填写)':
                st.session_state["coption1"] = st.text_input('请填写你的答案', key='coption1_key')

            coption2 = st.radio(
                '您偏好的项目',
                ('足浴按摩', '室内剧本杀', '美容美发', '寺庙祈福', '采茶、摘果子', '其他(请填写)')
            )
            st.session_state["coption2"] = coption2
            if st.session_state["coption2"] == '其他(请填写)':
                st.session_state["coption2"] = st.text_input('请填写你的答案', key='coption2_key')

            coption3 = st.radio(
                    '您偏好的酒店/度假村类型',
                    ('山间小舍', '最炫民族风', '网红民宿', '海景房', '其他(请填写)')
                )
            st.session_state["coption3"] = coption3
            if st.session_state["coption3"] == '其他(请填写)':
                st.session_state["coption3"] = st.text_input('请填写你的答案', key='coption3_key')

            coption4 = st.radio(
                        '如果让您来纪念本次旅途，您会选择',
                        ('特产', '各种美食调料包', '深度游，体验当地', '主题游，专注兴趣')
                    )
            st.session_state["coption4"] = coption4
            if st.session_state["coption4"] == '其他(请填写)':
                st.session_state["coption4"] = st.text_input('请填写你的答案', key='coption4_key')

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

                    full_response = ""
                    if st.session_state["form_selected"] == "form1":
                        input_text = f"请根据我给出的提示给我推荐一个适合我的旅游的地方，并且给我制定详细的计划：我的旅游预算是{st.session_state['budget']}元，出行人数是{st.session_state['number_of_people']}人，旅游天数是{st.session_state['number_of_days']}天，在旅游时我更喜欢{st.session_state['aoption1']}，我的旅游必备单品是{st.session_state['aoption2']}，到达目的地之后我的心情会因为{st.session_state['aoption3']}而变差，我的旅游目的主要是{st.session_state['aoption4']}，在结束我的旅途后我喜欢 {st.session_state['aoption5']}"

                    elif st.session_state["form_selected"] == "form2":
                        input_text = f"请根据我给出的提示给我推荐一个适合我的旅游的地方，并且给我制定详细的计划：我的旅游预算是{st.session_state['budget']}元，出行人数是{st.session_state['number_of_people']}人，旅游天数是{st.session_state['number_of_days']}天，我希望在{st.session_state['boption1']}之类的地方旅游，并且我喜欢以{st.session_state['boption2']}的方式观光，我喜欢{st.session_state['boption3']}之类的旅游项目，我希望我晚上在{st.session_state['boption4']}休息。"
                    else:
                        input_text = f"请根据我给出的提示给我推荐一个适合我的旅游的地方，并且给我制定详细的计划：我的旅游预算是{st.session_state['budget']}元，出行人数是{st.session_state['number_of_people']}人，旅游天数是{st.session_state['number_of_days']}天，我希望我旅游的时候可以躺在 {st.session_state['coption1']}，我喜欢{st.session_state['coption2']}之类的旅游项目，我希望我晚上在{st.session_state['coption3']}休息，通常我喜欢以{st.session_state['coption4']}的方式纪念我的旅途"
                elif skip_button:
                    # 当点击"填问卷太麻烦？一键开启盲盒旅行"按钮时，使用预备问卷的结果
                    input_text = f"给我安排一个详细的旅游计划：我的预算是 {st.session_state['budget']}元，一共有{st.session_state['number_of_people']}人，打算玩{st.session_state['number_of_days']}天"
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
