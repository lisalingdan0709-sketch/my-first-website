import streamlit as st
import time
import os

# 设置页面配置
st.set_page_config(page_title="我的个人主页", page_icon="🌟", layout="wide")

# --- 自定义 CSS (深蓝+绿色科技风) ---
st.markdown("""
<style>
    /* 引入 Google Fonts: Orbitron (标题) 和 Exo 2 (正文) */
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;700&family=Orbitron:wght@400;700&display=swap');

    /* 1. 全局背景色: 更有层次感的深蓝线性渐变 */
    .stApp {
        background-color: #020617;
        background-image: linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #020617 100%);
        background-attachment: fixed;
    }

    /* 2. 标题文字: 科技绿 + Orbitron 字体 */
    h1, h2, h3, h4 {
        color: #00FF9D !important;
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
    }
    
    /* 3. 普通文本: 浅灰 + Exo 2 字体 (清晰易读) */
    p, .stMarkdown, li, span, div {
        color: #E2E8F0 !important;
        font-family: 'Exo 2', sans-serif !important;
    }

    /* 4. 按钮样式: 镂空绿色边框，悬停发光 */
    .stButton > button {
        background-color: transparent;
        color: #00FF9D !important;
        border: 1px solid #00FF9D;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #00FF9D;
        color: #020617 !important;
        box-shadow: 0 0 15px rgba(0, 255, 157, 0.4);
    }

    /* 5. 教学卡片容器样式: Safari 兼容, 仅作用于教学卡片 */
    .teach-card {
        background-color: #0F172A !important;
        border: 3px solid #FFFFFF !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.5) !important;
        padding: 16px 14px;
        margin-bottom: 12px;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    }
    .teach-card:hover {
        border-color: #00FF9D !important;
        box-shadow: 0 18px 36px rgba(0, 255, 157, 0.3) !important;
        transform: translateY(-8px) !important;
    }
    .teach-card-link {
        display: block;
        text-decoration: none;
        color: inherit;
    }
    .teach-card .card-btn {
        display: inline-block;
        margin-top: 8px;
        padding: 8px 14px;
        color: #00FF9D !important;
        border: 1px solid #00FF9D;
        border-radius: 6px;
        font-family: 'Orbitron', sans-serif !important;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    .teach-card .card-btn:hover {
        background-color: #00FF9D;
        color: #020617 !important;
        box-shadow: 0 0 15px rgba(0, 255, 157, 0.4);
    }
    
    /* 6. 分割线 */
    hr {
        border-color: #1E293B;
    }
    
    /* 7. 输入框样式 */
    .stTextInput > div > div > input {
        background-color: #1E293B;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# --- 数据准备 ---
# 为了演示，我补充到了4个卡片
cards = [
    {
        "id": 1,
        "task": "搭建第一个 Python 脚本",
        "desc": "Python 基础语法入门",
        "learned": "掌握了 Python 的基础语法，变量定义以及 print 函数的使用。",
        "review": "开始时对环境配置不熟悉，花费了很多时间。下次应该先阅读官方文档。",
        "media_type": "image",
        "media_caption": "成功运行 Hello World 的截图"
    },
    {
        "id": 2,
        "task": "Streamlit 网页开发",
        "desc": "快速搭建数据可视化应用",
        "learned": "学会了 st.write, st.columns 等布局组件的使用。",
        "review": "布局调整需要多尝试，Grid 布局很实用。",
        "media_type": "image",
        "media_caption": "网页布局草图"
    },
    {
        "id": 3,
        "task": "制作教学视频",
        "desc": "多媒体内容创作",
        "learned": "学习了剪辑软件的基本操作，以及如何通过 AI 生成字幕。",
        "review": "视频节奏感还需要加强，声音录制需要更安静的环境。",
        "media_type": "video",
        "media_caption": "我的教学演示视频"
    },
    {
        "id": 4,
        "task": "AI 知识库问答",
        "desc": "RAG 技术与 LLM 应用",
        "learned": "理解了向量数据库和 Prompt Engineering 的基本概念。",
        "review": "Token 限制需要注意，上下文管理很重要。",
        "media_type": "image",
        "media_caption": "RAG 流程图"
    },
    {
        "id": 5,
        "task": "Prompt 设计与优化",
        "desc": "让模型更好理解你的意图",
        "learned": "掌握了提示词结构化思路和常见优化技巧。",
        "review": "需要多做实验，收集对比效果。",
        "media_type": "image",
        "media_caption": "Prompt 结构示意"
    }
]

# --- 状态管理 (用于页面跳转) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home' # 默认显示首页
if 'selected_card_id' not in st.session_state:
    st.session_state.selected_card_id = None

def go_to(page_name):
    st.session_state.page = page_name
    if page_name == 'home':
        if hasattr(st, "query_params"):
            st.query_params.clear()
        else:
            st.experimental_set_query_params()

def read_query_params():
    if hasattr(st, "query_params"):
        params = st.query_params
    else:
        params = st.experimental_get_query_params()
    page = params.get("page")
    card = params.get("card")
    if isinstance(page, list):
        page = page[0]
    if isinstance(card, list):
        card = card[0]
    if page:
        st.session_state.page = page
    if card:
        try:
            st.session_state.selected_card_id = int(card)
        except ValueError:
            st.session_state.selected_card_id = None

read_query_params()

# --- 页面渲染逻辑 ---

# 1. 首页
if st.session_state.page == 'home':
    # 首页顶部 Banner 图片 (AI 科技风)
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=90&w=2400&h=500&auto=format&fit=crop", use_container_width=True)
    
    st.title("🏠 小凌同学的个人学习中心")
    st.write("欢迎来到我的数字花园，这里记录了我的AI成长轨迹。")
    st.divider()

    # --- 板块 1: 个人信息 ---
    st.subheader("1️⃣ 个人信息")
    with st.container(border=True):
        col1, col2 = st.columns([1, 5])
        with col1:
            if os.path.exists("avatar.jpg"):
                st.image("avatar.jpg", use_container_width=True)
            else:
                st.info("请放入 avatar.jpg")
        with col2:
            st.markdown("### 我是 小凌同学")
            st.write("终身学习者")
            st.write("热衷于将 AI 技术应用于生活方方面面，提升效率。")
            if st.button("查看完整名片"):
                go_to('profile')
                st.rerun()

    # --- 板块 2: 教学卡片 (简略展示) ---
    st.subheader("2️⃣ 教学卡片")
    # 使用列布局展示第一排4个卡片
    row1 = st.columns(4)
    for i, card in enumerate(cards[:4]):
        with row1[i]:
            st.markdown(f"""
            <a class="teach-card-link" href="?page=card_detail&card={card['id']}">
              <div class="teach-card">
                <div><strong>卡片 {card['id']}</strong></div>
                <div><strong>{card['task']}</strong></div>
                <div>{card['desc']}</div>
                <span class="card-btn">查看详情</span>
              </div>
            </a>
            """, unsafe_allow_html=True)

    # 第二排: 卡片5放在卡片1正下方
    row2 = st.columns(4)
    card = cards[4]
    with row2[0]:
        st.markdown(f"""
        <a class="teach-card-link" href="?page=card_detail&card={card['id']}">
          <div class="teach-card">
            <div><strong>卡片 {card['id']}</strong></div>
            <div><strong>{card['task']}</strong></div>
            <div>{card['desc']}</div>
            <span class="card-btn">查看详情</span>
          </div>
        </a>
        """, unsafe_allow_html=True)

    # --- 板块 3: AI 问答 ---
    st.subheader("3️⃣ AI 知识库")
    with st.container(border=True):
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown("#### 🤖 AI 助手")
            st.write("我已经学习了上述所有卡片的内容，你可以考考我！")
        with c2:
            st.write("")
            if st.button("进入 AI 问答", use_container_width=True):
                go_to('ai_chat')
                st.rerun()

# 2. 个人名片详情页
elif st.session_state.page == 'profile':
    if st.button("⬅️ 返回首页"):
        go_to('home')
        st.rerun()
    
    st.title("👋 我的个人名片")
    col1, col2 = st.columns([1, 2])
    with col1:
        if os.path.exists("avatar.jpg"):
            st.image("avatar.jpg", use_container_width=True)
        else:
            st.info("请放入 avatar.jpg")
        st.metric(label="学习天数", value="120 天", delta="持续进步中")
    with col2:
        st.header("关于我")
        st.write("""
        你好！我是 **[你的名字]**。
        这里是我的个人介绍文案。我热衷于学习新技术，并致力于将 AI 应用于教学和日常生活中。
        - 📍 **坐标**: 中国
        - 💼 **职业**: 开发者 / 讲师 / 学习者
        - 📧 **联系方式**: email@example.com
        """)
        st.subheader("我的技能")
        st.markdown("`Python` `AI/LLM` `Web 开发` `教学设计`")

# 3. 教学卡片详情页
elif st.session_state.page == 'card_detail':
    if st.button("⬅️ 返回首页"):
        go_to('home')
        st.rerun()
    
    # 获取当前选中的卡片数据
    current_id = st.session_state.selected_card_id
    card = next((c for c in cards if c['id'] == current_id), None)
    
    if card:
        st.title(f"📚 教学卡片 {card['id']}: {card['task']}")
        with st.container(border=True):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"**🎯 任务内容:** {card['task']}")
                st.markdown(f"**💡 我学到了什么:**\n{card['learned']}")
                st.markdown(f"**🔄 我的复盘:**\n{card['review']}")
            with c2:
                st.write("📸 **成功展示:**")
                st.warning(f"此处展示 {card['media_type']}: {card['media_caption']}")
    else:
        st.error("未找到卡片信息")

# 4. AI 问答详情页
elif st.session_state.page == 'ai_chat':
    if st.button("⬅️ 返回首页"):
        go_to('home')
        st.rerun()

    st.title("🤖 AI 知识库助手")
    st.caption("这个 AI 已经学习了我的知识库，你可以问我关于我所学内容的任何问题。")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("请输入你的问题..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        response_text = f"这是一个模拟回复。我已经收到了关于“{prompt}”的问题。根据我的知识库（教学卡片内容），我的回答是......"
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for chunk in response_text:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
                time.sleep(0.02)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
