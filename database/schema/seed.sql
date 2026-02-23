-- 插入提示词分类
INSERT OR IGNORE INTO categories (name) VALUES
('未分类'),
('代码审查'),
('Bug 分析'),
('技术方案'),
('代码重构'),
('接口设计');

-- 插入提示词（只创建条目，不存内容）
INSERT OR IGNORE INTO prompts (category_id, title, current_version, description, created_at, updated_at) VALUES
(2, '代码 Review 模板', 1, '用于对已有代码进行专业、结构化 Code Review', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, 'Bug 根因分析模板', 1, '用于排查线上问题', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, '技术方案拆解模板', 1, '将业务需求拆解为可落地技术方案', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, '现有代码重构建议模板', 1, '针对现有代码提出改进建议', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, '接口设计与文档生成模板', 1, '根据功能生成接口设计与文档', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


-- 插入提示词版本内容
INSERT OR IGNORE INTO prompt_versions (prompt_id, content, version, created_at) VALUES
-- 模板 1
(1, '你是一名经验丰富的 {{language}} 资深工程师。
请对以下代码进行专业 Code Review：
{{code}}
项目背景：{{context}}
请重点关注：{{focus}}
输出请严格按以下结构：
1. 总体评价（不超过 3 句话）
2. 主要问题（按严重程度排序）
3. 可优化建议（给出明确修改方向）
4. 潜在风险（如并发、安全、边界情况）
如果代码质量已达生产可用水平，也请明确说明原因。
卖点：稳定、不会“水回答”', 1, CURRENT_TIMESTAMP),

-- 模板 2
(2, '你是一名擅长排查线上问题的工程专家。
错误信息：{{error}}
相关代码：{{code}}
运行环境：{{env}}
预期行为：{{expected}}
请按以下步骤分析：
1. 可能的根因（列出 2–3 个）
2. 如何验证每个根因
3. 最可能的根因判断
4. 推荐的修复方案
避免给出泛泛而谈的建议。', 1, CURRENT_TIMESTAMP),

-- 模板 3
(3, '你是一名负责技术方案设计的后端工程师。
业务需求：{{requirement}}
技术栈：{{stack}}
约束条件：{{constraints}}
请输出一份可落地的技术方案，包含：
1. 核心功能拆解
2. 模块划分与职责
3. 关键技术选型理由
4. 潜在风险与应对
5. 简要实现步骤
方案应以工程可落地为优先。', 1, CURRENT_TIMESTAMP),

-- 模板 4
(4, '以下是当前代码：{{code}}
当前主要问题：{{problem}}
重构目标：{{goal}}
请给出：
1. 是否有必要重构（明确判断）
2. 推荐的重构方向
3. 分步骤重构建议（避免一次性推翻）
4. 重构后的预期收益
不要建议“全部重写”。', 1, CURRENT_TIMESTAMP),

-- 模板 5
(5, '请基于以下功能设计接口：
功能描述：{{feature}}
接口风格：{{api_style}}
鉴权方式：{{auth}}
输出内容包括：
1. 接口列表（路径 / 方法）
2. 请求参数说明
3. 返回结构示例
4. 错误码设计
接口设计应符合工程实践。', 1, CURRENT_TIMESTAMP);
