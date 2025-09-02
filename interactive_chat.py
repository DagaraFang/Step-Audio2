#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step-Audio2 交互式对话脚本
内存优化版本，支持文本对话
"""

import sys
from stepaudio2 import StepAudio2

def main():
    print("🎤 Step-Audio2 交互式对话")
    print("=" * 50)
    print("正在加载模型，请稍等...")
    
    try:
        # 加载模型
        model = StepAudio2('Step-Audio-2-mini')
        print("✅ 模型加载完成！")
        print("💡 输入 'quit' 或 'exit' 退出程序")
        print("=" * 50)
        
        # 系统提示词
        system_prompt = "你的名字叫做小跃，是由阶跃星辰公司训练出来的语音大模型。你情感细腻，观察能力强，擅长分析用户的内容，并作出善解人意的回复。请用中文与用户交流。"
        
        # 对话历史
        conversation_history = [
            {"role": "system", "content": system_prompt}
        ]
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n👤 你: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                    print("\n👋 再见！")
                    break
                
                # 添加用户消息到历史
                conversation_history.append({
                    "role": "human", 
                    "content": user_input
                })
                
                # 添加助手回复占位符
                conversation_history.append({
                    "role": "assistant", 
                    "content": None
                })
                
                print("\n🤖 小跃: ", end="", flush=True)
                
                # 生成回复
                tokens, text, _ = model(
                    conversation_history, 
                    max_new_tokens=256, 
                    temperature=0.7, 
                    repetition_penalty=1.05, 
                    top_p=0.9, 
                    do_sample=True
                )
                
                print(text)
                
                # 更新对话历史
                conversation_history[-1]["content"] = text
                
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断，再见！")
                break
            except Exception as e:
                print(f"\n❌ 错误: {e}")
                print("请重试...")
                # 移除最后一个未完成的回复
                if conversation_history and conversation_history[-1]["content"] is None:
                    conversation_history.pop()
                    
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())