import openai
from backend.app.core.config import settings

SYSTEM_INSTRUCTION = """
你是一位资深 Prompt Engineer，请将用户提供的提示词优化为结构化版本。
仅返回优化后的 Prompt 内容，不要包含任何多余的解释文字。
"""

def get_llm_client(provider: str):
    """ 获取 LLM 客户端 """
    if provider in ["deepseek", "openai", "ollama"]:
        return openai.OpenAI(
            api_key=settings.API_KEY, 
            base_url=settings.BASE_URL
        )
    # 如果后续增加了不支持 OpenAI SDK 的厂商，则需要增加对应的客户端
    # elif provider == "xxx":
    #     return xxx.Client(api_key=api_key, base_url=base_url)
    raise ValueError(f"不支持的提供商: {provider}")

def optimization_prompt(prompt: str):
    """ 流式获取 AI 生成的优化结果 """
    try:
        # 获取 LLM 客户端
        client = get_llm_client(settings.LLM_PROVIDER)
        # 发送请求调用 API
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTION},
                {"role": "user", "content": f"请优化以下提示词：\n{prompt}"}
            ],
            temperature=0.7,
            stream=True 
        )
        for chunk in response:
            # 提取当前数据块的文本内容
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except Exception as e:
        err_str = str(e).lower()
        if "authentication" in err_str or "api_key" in err_str or "401" in err_str:
            yield "ERR_AUTH: 验证失败，请检查是否正确设置 API Key"
        else:
            yield f"AI 服务响应异常: {str(e)}"
    
    