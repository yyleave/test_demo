import os
from openai import OpenAI
import asyncio
import os

# Install SDK: pip install openai

# 初始化OpenAI客户端（兼容火山方舟）
client = OpenAI(
    # The base URL for model invocation
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    # Get API Key：https://console.volcengine.com/ark/region:ark+cn-beijing/apikey
    api_key=os.getenv('ARK_API_KEY'),
)

completion = client.chat.completions.create(
    # Replace with Model ID
    model="doubao-seed-2-0-lite-260215",
    messages=[
        {"role": "user", "content": "请将下面内容进行结构化处理：火山方舟是火山引擎推出的大模型服务平台，提供模型训练、推理、评测、精调等全方位功能与服务，并重点支撑大模型生态。 火山方舟通过稳定可靠的安全互信方案，保障模型提供方的模型安全与模型使用者的信息安全，加速大模型能力渗透到千行百业，助力模型提供方和使用者实现商业新增长。"},
    ],
    # thinking={"type": "disabled"}, #  Manually disable deep thinking
)

print(completion.choices[0].message.content)


response = client.responses.create(
    model="doubao-seed-2-0-lite-260215",
    input=[
        {
            "role": "user",
            "content": [

                {
                    "type": "input_image",
                    "image_url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png"
                },
                {
                    "type": "input_text",
                    "text": "Which model series supports image input?"
                },
            ],
        }
    ]
)

print(response)

async def main():
    # upload pdf file
    print("Upload pdf file")
    file = await client.files.create(
        # replace with your local pdf path
        file=open("/Users/doc/demo.pdf", "rb"),
        purpose="user_data"
    )
    print(f"File uploaded: {file.id}")

    # Wait for the file to finish processing
    await client.files.wait_for_processing(file.id)
    print(f"File processed: {file.id}")

    response = await client.responses.create(
        model="doubao-seed-2-0-lite-260215",
        input=[
            {"role": "user", "content": [
                {
                    "type": "input_file",
                    "file_id": file.id  # ref pdf file id
                },
                {
                    "type": "input_text",
                    "text": "按段落给出文档中的文字内容，以JSON格式输出，包括段落类型（type）、文字内容（content）信息。"
                }
            ]},
        ],
    )
    print(response)


asyncio.run(main())


tools = [{
    "type": "web_search",
    "max_keyword": 2,  
}]

# 创建一个对话请求
response = client.responses.create(
    model="doubao-seed-1-6-250615",
    input=[{"role": "user", "content": "今天有什么热点新闻？"}],
    tools=tools,
)

print(response)

response = client.responses.create(
    model="doubao-seed-1-6-251015",
    tools=[
        {
            "type": "mcp",
            "server_label": "deepwiki",
            "server_url": "https://mcp.deepwiki.com/mcp",
            "require_approval": "never"
        }
    ],
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "看一下volcengine/ai-app-lab这个repo的文档"
                }
            ]
        }
    ],
    extra_headers={"ark-beta-mcp": "true"},
    stream=True  # 流式获取结果
)

# 打印响应结果
for chunk in response:
    if hasattr(chunk, 'delta'):
        print(chunk.delta, end="", flush=True)


messages = [
    {"role": "user", "content": "北京和上海今天的天气如何？"}
]
# 步骤1: 定义工具
tools = [{
  "type": "function",
  "function": {
    "name": "get_current_weather",
    "description": "获取指定地点的天气信息",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "地点的位置信息，例如北京、上海"
        },
        "unit": {
          "type": "string",
          "enum": ["摄氏度", "华氏度"],
          "description": "温度单位"
        }
      },
      "required": ["location"]
    }
  }
}]
def get_current_weather(location: str, unit="摄氏度"):
    # 实际调用天气查询 API 的逻辑
    # 此处为示例，返回模拟的天气数据
    return f"{location}今天天气晴朗，温度 25 {unit}。"
while True:
    # 步骤2: 发起模型请求，由于模型在收到工具执行结果后仍然可能有函数调用意愿，因此需要多次请求
    completion: ChatCompletion = client.chat.completions.create(
    model="doubao-seed-2-0-lite-260215",
    messages=messages,
    tools=tools
    )
    resp_msg = completion.choices[0].message
    # 展示模型中间过程的回复内容
    print(resp_msg.content)
    if completion.choices[0].finish_reason != "tool_calls":
        # 模型最终总结，没有调用工具意愿
        break
    messages.append(completion.choices[0].message.model_dump())
    tool_calls = completion.choices[0].message.tool_calls
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        if tool_name == "get_current_weather":
            # 步骤 3：调用外部工具
            args = json.loads(tool_call.function.arguments)
            tool_result = get_current_weather(**args)
            # 步骤 4：回填工具结果，并获取模型总结回复
            messages.append(
                {"role": "tool", "content": tool_result, "tool_call_id": tool_call.id}
            )

completion = client.chat.completions.create(
    # Replace with Model ID
    model = "doubao-seed-2-0-lite-260215",
    messages=[
        {"role": "user", "content": "我要研究深度思考模型与非深度思考模型区别的课题，怎么体现我的专业性"}
    ]
)
# When deep thinking is triggered, print the chain-of-thought content
if hasattr(completion.choices[0].message, 'reasoning_content'):
    print(completion.choices[0].message.reasoning_content)
print(completion.choices[0].message.content)

completion = client.chat.completions.create(
    # Replace with Model ID
    model = "doubao-seed-2-0-lite-260215",
    messages=[
        {"role": "user", "content": "研究深度思考模型与非深度思考模型区别"},
        {"role": "assistant", "content": "推理模型主要依靠逻辑、规则或概率等进行分析、推导和判断以得出结论或决策，非推理模型则是通过模式识别、统计分析或模拟等方式来实现数据描述、分类、聚类或生成等任务而不依赖显式逻辑推理。"},
        {"role": "user", "content": "我要研究深度思考模型与非深度思考模型区别的课题，怎么体现我的专业性"},
    ],
)

if hasattr(completion.choices[0].message, 'reasoning_content'):
    print(completion.choices[0].message.reasoning_content)
print(completion.choices[0].message.content)

file = client.files.create(
    # replace with your local video path
    file=open("/Users/doc/demo.mp4", "rb"),
    purpose="user_data",
    preprocess_configs={
        "video": {
            "fps": 0.3,  # define the sampling fps of the video, default is 1.0
        }
    }
)
print(file)


class Step(BaseModel):
    explanation: str  # 步骤说明
    output: str       # 步骤计算结果

# 定义最终响应模型（包含分步过程和最终答案）
class MathResponse(BaseModel):
    steps: list[Step]       # 解题步骤列表
    final_answer: str       # 最终答案

# 调用方舟模型生成响应（自动解析为指定模型）
completion = client.beta.chat.completions.parse(
    model="doubao-seed-1-6-250615",  # 具体模型需替换为实际可用模型
    messages=[
        {"role": "system", "content": "你是一位数学辅导老师，需详细展示解题步骤"},
        {"role": "user", "content": "用中文解方程组：8x + 9 = 32 和 x + y = 1"}
    ],
    response_format=MathResponse,  # 指定响应解析模型
    extra_body={
         "thinking": {
             "type": "disabled" # 不使用深度思考能力
             # "type": "enabled" # 使用深度思考能力
         }
     }
)

# 提取解析后的结构化响应
resp = completion.choices[0].message.parsed

# 打印格式化的JSON结果
print(resp.model_dump_json(indent=2))

completion = client.chat.completions.create(
    model="doubao-seed-1-6-251015",  # Replace with Model ID
    messages=[
        {"role": "user", "content": "常见的十字花科植物有哪些？json输出"}
    ],
    response_format={"type":"json_object"},
    thinking={"type": "disabled"},# 不使用深度思考能力
)

# 打印原始响应内容
print(completion.choices[0].message.content)