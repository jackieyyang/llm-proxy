/* ============================================================
 * Schema: llm_proxy
 * ============================================================ */

CREATE SCHEMA IF NOT EXISTS llm_proxy;

/* ============================================================
 * 1. 模型提供方表
 * ============================================================ */
CREATE TABLE llm_proxy.tb_provider (
    id BIGSERIAL PRIMARY KEY,
    provider_name VARCHAR(64) NOT NULL,
    api_key VARCHAR(255) NOT NULL,
    base_url VARCHAR(255) NOT NULL,
    status INT DEFAULT 1,
    remark VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE llm_proxy.tb_provider IS '模型提供方（OpenAI / Azure / Anthropic 等）';
COMMENT ON COLUMN llm_proxy.tb_provider.provider_name IS '提供方名称';
COMMENT ON COLUMN llm_proxy.tb_provider.api_key IS '提供方 API Key';
COMMENT ON COLUMN llm_proxy.tb_provider.base_url IS 'API Base URL';
COMMENT ON COLUMN llm_proxy.tb_provider.status IS '状态：1-启用 0-禁用';
COMMENT ON COLUMN llm_proxy.tb_provider.remark IS '备注说明';

/* ============================================================
 * 2. 模型部署表
 * ============================================================ */
CREATE TABLE llm_proxy.tb_model_deployment (
    id BIGSERIAL PRIMARY KEY,
    provider_id BIGINT NOT NULL,
    deployment_name VARCHAR(100) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    rpm INT DEFAULT 0,
    tpm INT DEFAULT 0,
    status INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE llm_proxy.tb_model_deployment IS '模型部署配置（Provider 下的模型实例）';
COMMENT ON COLUMN llm_proxy.tb_model_deployment.provider_id IS '所属模型提供方 ID（逻辑关联）';
COMMENT ON COLUMN llm_proxy.tb_model_deployment.deployment_name IS '部署名称或别名';
COMMENT ON COLUMN llm_proxy.tb_model_deployment.model_name IS '模型名称（gpt-4o / gpt-4.1 等）';
COMMENT ON COLUMN llm_proxy.tb_model_deployment.rpm IS '部署级 RPM 限制';
COMMENT ON COLUMN llm_proxy.tb_model_deployment.tpm IS '部署级 TPM 限制';
COMMENT ON COLUMN llm_proxy.tb_model_deployment.status IS '状态：1-启用 0-禁用';

/* ============================================================
 * 3. 用户表
 * ============================================================ */
CREATE TABLE llm_proxy.tb_user (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    api_key VARCHAR(64) NOT NULL UNIQUE,
    description TEXT,
    status INT DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE llm_proxy.tb_user IS 'LLM Proxy 用户';
COMMENT ON COLUMN llm_proxy.tb_user.username IS '用户名';
COMMENT ON COLUMN llm_proxy.tb_user.api_key IS '用户访问 API Key';
COMMENT ON COLUMN llm_proxy.tb_user.description IS '用户描述';
COMMENT ON COLUMN llm_proxy.tb_user.status IS '状态：1-启用 0-禁用';

/* ============================================================
 * 4. 用户模型配额表
 * ============================================================ */
CREATE TABLE llm_proxy.tb_user_quota (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    rpm INT DEFAULT 0,
    tpm INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE llm_proxy.tb_user_quota IS '用户模型配额（逻辑关联 tb_user）';
COMMENT ON COLUMN llm_proxy.tb_user_quota.user_id IS '用户 ID（逻辑关联）';
COMMENT ON COLUMN llm_proxy.tb_user_quota.model_name IS '模型名称';
COMMENT ON COLUMN llm_proxy.tb_user_quota.rpm IS '用户级 RPM 限制';
COMMENT ON COLUMN llm_proxy.tb_user_quota.tpm IS '用户级 TPM 限制';

/* ============================================================
 * 5. 使用记录表（调用日志）
 * ============================================================ */
CREATE TABLE llm_proxy.tb_usage (
    id BIGSERIAL PRIMARY KEY,
    trace_id VARCHAR(64) NOT NULL,
    user_id BIGINT NOT NULL,
    provider_id BIGINT NOT NULL,
    model_deployment_id BIGINT NOT NULL,
    prompt_tokens INT DEFAULT 0,
    completion_tokens INT DEFAULT 0,
    total_tokens INT DEFAULT 0,
    proxy_latency_ms BIGINT DEFAULT 0,
    provider_latency_ms BIGINT DEFAULT 0,
    first_token_latency_ms BIGINT DEFAULT 0,
    proxy_code INT,
    provider_code INT,
    created_at TIMESTAMPTZ DEFAULT now()
);

COMMENT ON TABLE llm_proxy.tb_usage IS 'LLM 调用使用日志（高并发写入）';
COMMENT ON COLUMN llm_proxy.tb_usage.trace_id IS '请求 Trace ID';
COMMENT ON COLUMN llm_proxy.tb_usage.user_id IS '调用用户 ID（逻辑关联）';
COMMENT ON COLUMN llm_proxy.tb_usage.provider_id IS '模型提供方 ID（逻辑关联）';
COMMENT ON COLUMN llm_proxy.tb_usage.model_deployment_id IS '模型部署 ID（逻辑关联）';
COMMENT ON COLUMN llm_proxy.tb_usage.prompt_tokens IS 'Prompt Token 数';
COMMENT ON COLUMN llm_proxy.tb_usage.completion_tokens IS 'Completion Token 数';
COMMENT ON COLUMN llm_proxy.tb_usage.total_tokens IS '总 Token 数';
COMMENT ON COLUMN llm_proxy.tb_usage.proxy_latency_ms IS 'Proxy 处理耗时（毫秒）';
COMMENT ON COLUMN llm_proxy.tb_usage.provider_latency_ms IS 'Provider 响应耗时（毫秒）';
COMMENT ON COLUMN llm_proxy.tb_usage.first_token_latency_ms IS '首 Token 延迟（毫秒）';
COMMENT ON COLUMN llm_proxy.tb_usage.proxy_code IS 'Proxy 返回码';
COMMENT ON COLUMN llm_proxy.tb_usage.provider_code IS 'Provider 返回码';