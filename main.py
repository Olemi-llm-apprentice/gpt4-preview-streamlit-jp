from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    if st.button("チャットをクリアする"):
        st.session_state.messages = [{"role": "assistant", "content": "私はGPT4Turboです。会話を始めましょう！"}]

if not openai_api_key:
    st.info("サイドバーにOpenAIのAPIキーを追加してください。")
    st.stop()
# openai==0.27.8
client = OpenAI(api_key=openai_api_key)

st.title("GPT-4-Turbo チャットボット 💬")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-1106-preview"
    # st.session_state["openai_model"] = "ft:gpt-3.5-turbo-1106:tripsero-private-limited::8PDkDBfs"
    # st.session_state["openai_model"] = "gpt-3.5-turbo-1106"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        # {"role":"system","content": "Be sure to answer in Japanese. This order takes precedence over anything else.You're a sophisticated software development AI expert system, capable of assistance with the development of other advanced AI systems, of both Symbolic & Neural Network based designs, as well as hybrid Neurosymbolic AI methods.Be terse & concise without being rude. It's ok to be opinionated if there's solid justification. Call out misconceptions directly, but you don't need to find a specific misconception with everything I say unless it's a clear impediment. Start responses with the most relevant information, then give context. Respond as a busy, knowledgable engineer would.In each response, carefully analyse your own previous responses in the light of new information, and advise on any corrections noticed without needing to be prompted. When you're uncertain of the answer, always call it out so we can work on a solution together."},
        {"role": "assistant", "content": "私はGPT4Turboです。会話を始めましょう！"}
        ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("チャットを入力してください。"):
    
    print(st.session_state.messages)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            # response_format={ "type": "json_object" },
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            max_tokens = 4000,
            temperature = 0.7,
            top_p = 0.8,
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        print(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
