from __future__ import annotations

import os

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

from agent import MODEL_NAME, get_graph, run_agent
from langchain_core.messages import HumanMessage, AIMessage

APP_TITLE = "XanhSM CRM Assistant"


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --border: #b9decf;
                --brand: #007a53;
                --brand-dark: #05553b;
                --text: #153126;
                --muted: #4b6b5f;
            }

            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(0, 122, 83, 0.18), transparent 28%),
                    linear-gradient(180deg, #f8fdfb 0%, #eef8f3 100%);
            }

            .hero {
                padding: 1.5rem;
                border: 1px solid var(--border);
                border-radius: 24px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(228, 245, 237, 0.95));
                box-shadow: 0 20px 50px rgba(4, 84, 57, 0.08);
                color: var(--text);
                margin-bottom: 1rem;
            }

            .hero h1 {
                margin: 0;
                color: var(--brand-dark);
                font-size: 2rem;
            }

            .hero p {
                margin: 0.6rem 0 0;
                color: var(--muted);
                font-size: 1rem;
            }

            .chip-row {
                display: flex;
                gap: 0.75rem;
                flex-wrap: wrap;
                margin-top: 1rem;
            }

            .chip {
                padding: 0.45rem 0.9rem;
                border-radius: 999px;
                background: rgba(0, 122, 83, 0.1);
                border: 1px solid rgba(0, 122, 83, 0.18);
                color: var(--brand-dark);
                font-size: 0.92rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _init_session_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("pending_prompt", None)


def _render_sidebar() -> None:
    with st.sidebar:
        st.subheader("Cau hinh")
        st.write(f"Model: `{MODEL_NAME}`")
        st.write("Provider hien tai duoc nap tu `.env`.")

        if os.getenv("OPENAI_API_KEY"):
            st.success("Da tim thay OPENAI_API_KEY")
        else:
            st.error("Chua tim thay OPENAI_API_KEY trong moi truong")

        if st.button("Xoa lich su chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

        st.divider()
        st.caption("Goi y")
        st.caption("- Tra cuu chuyen di theo ma")
        st.caption("- Tao ticket ho tro cho khach hang")


def _render_header() -> None:
    st.markdown(
        """
        <section class="hero">
            <h1>XanhSM CRM Assistant</h1>
            <p>Frontend Streamlit cho chatbot ho tro tra cuu chuyen di va tao ticket cham soc khach hang.</p>
            <div class="chip-row">
                <span class="chip">Chat realtime</span>
                <span class="chip">LangGraph agent</span>
                <span class="chip">Tool calling</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def _append_message(role: str, content: str) -> None:
    if role == "user":
        msg = HumanMessage(content=content)
    elif role == "assistant":
        msg = AIMessage(content=content)
    else:
        raise ValueError(f"Unknown role: {role}")
    
    st.session_state.messages.append(msg)


def _handle_prompt(prompt: str) -> None:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Agent dang xu ly..."):
            try:
                messages = st.session_state.messages.copy()
                answer, updated_messages = run_agent(prompt, messages, graph=get_graph())
                st.session_state.messages = updated_messages
            except Exception as exc:  # pragma: no cover - UI fallback
                answer = f"Khong the xu ly yeu cau luc nay.\n\nChi tiet loi: `{exc}`"
            if answer.strip():
                st.markdown(answer)


def _queue_prompt(prompt: str) -> None:
    st.session_state.pending_prompt = prompt
    st.rerun()


def _render_example_prompts() -> None:
    st.caption("Thu nhanh voi mot trong cac mau ben duoi:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Tra cuu ma chuyen 123", use_container_width=True):
            _queue_prompt("Tra cuu chuyen di voi ma 123")

    with col2:
        if st.button("Tao ticket that lac do", use_container_width=True):
            _queue_prompt("Toi bi that lac do tren chuyen di 123, hay tao ticket ho tro giup toi")


def _render_messages() -> None:
    if not st.session_state.messages:
        st.info("Chua co hoi thoai. Hay gui cau hoi o o nhap ben duoi.")
        return

    for message in st.session_state.messages:
        if isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            if not message.content.strip():
                continue  # skip empty assistant messages
            role = "assistant"
        else:
            continue  # skip tool messages
        with st.chat_message(role):
            st.markdown(message.content)


def main() -> None:
    st.set_page_config(
        page_title=APP_TITLE,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_styles()
    _init_session_state()
    _render_sidebar()
    _render_header()
    _render_example_prompts()
    _render_messages()

    prompt = st.chat_input("Nhap noi dung can ho tro...")
    active_prompt = prompt or st.session_state.pending_prompt
    if active_prompt:
        st.session_state.pending_prompt = None
        _handle_prompt(active_prompt)
        st.rerun()


def _run_entrypoint() -> None:
    if get_script_run_ctx(suppress_warning=True) is None:
        print(
            "Day la ung dung Streamlit. Hay chay bang lenh:\n"
            "python -m streamlit run app.py"
        )
        raise SystemExit(0)

    main()


if __name__ == "__main__":
    _run_entrypoint()
