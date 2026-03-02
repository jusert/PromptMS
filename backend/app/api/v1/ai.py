from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.app.service.ai import optimization_prompt
from backend.app.models import OptimizeRequest,ConfigUpdate
from backend.app.core.config import settings, update_env_file

router = APIRouter()


@router.post("/optimize")
async def api_optimize_prompt(data: OptimizeRequest):
    if not data.prompt.strip():
        raise HTTPException(status_code=400, detail="提示词不能为空")
    # 定义一个内部生成器，用于格式化输出
    def generate():
        # 调用上面写的流式函数
        for chunk in optimization_prompt(data.prompt):
            # 这里的格式可以根据前端需求调整
            # 直接返回原始文本或符合 SSE 格式的 "data: content\n\n"
            yield chunk
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/update-settings")
async def update_settings(data: ConfigUpdate):
    try:
        # 准备更新字典 (映射前端字段到 .env 字段)
        updates = {}
        if data.api_key:
            settings.API_KEY = data.api_key
            updates["API_KEY"] = data.api_key
        if data.base_url:
            settings.BASE_URL = data.base_url
            updates["BASE_URL"] = data.base_url
        if data.provider:
            settings.LLM_PROVIDER = data.provider
            updates["LLM_PROVIDER"] = data.provider
        # 写入文件持久化
        update_env_file(updates)
        return {"message": "配置更新成功并已保存到本地"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))