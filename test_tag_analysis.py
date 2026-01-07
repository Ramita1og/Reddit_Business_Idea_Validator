"""
测试标签分析功能
"""
import asyncio
import json
from datetime import datetime
from agents.skills.analyzer_skills import analyze_comments_with_tags_skill
from models.business_models import TagSystemGeneration


async def test_tag_analysis():
    """测试标签分析功能"""
    
    # 创建测试数据 - 模拟 Reddit AI 技术讨论
    test_posts = [
        {
            "note_id": "test1",
            "title": "DeepSeek R1 vs GPT-4: A Technical Comparison",
            "subreddit": "r/LocalLLaMA",
            "content": "Comparing the reasoning capabilities of DeepSeek R1 and GPT-4...",
            "score": 150,
            "upvote_ratio": 0.95,
            "comments_data": [
                {
                    "comment_id": "c1",
                    "user_nickname": "dev123",
                    "content": "DeepSeek R1 has better reasoning for coding tasks, especially for complex algorithms. The model architecture seems more efficient.",
                    "score": 45,
                    "created_utc": 1736200000
                },
                {
                    "comment_id": "c2",
                    "user_nickname": "researcher_ai",
                    "content": "I've been using it for academic research. The mathematical reasoning is impressive, but sometimes it hallucinates on niche topics.",
                    "score": 32,
                    "created_utc": 1736200100
                },
                {
                    "comment_id": "c3",
                    "user_nickname": "ml_engineer",
                    "content": "The open-source nature is great for customization. We've fine-tuned it for our specific use case and it performs better than GPT-4.",
                    "score": 28,
                    "created_utc": 1736200200
                }
            ],
            "analysis": {
                "relevant": True,
                "summary": "Technical discussion comparing DeepSeek R1 and GPT-4"
            }
        },
        {
            "note_id": "test2",
            "title": "Deploying DeepSeek R1 on Local Hardware",
            "subreddit": "r/LocalLLaMA",
            "content": "Guide on how to run DeepSeek R1 locally...",
            "score": 89,
            "upvote_ratio": 0.92,
            "comments_data": [
                {
                    "comment_id": "c4",
                    "user_nickname": "hardware_enthusiast",
                    "content": "Running on RTX 4090 with 24GB VRAM. Need to use 4-bit quantization to fit. Performance is decent but slow on large prompts.",
                    "score": 56,
                    "created_utc": 1736200300
                },
                {
                    "comment_id": "c5",
                    "user_nickname": "developer_local",
                    "content": "The documentation is good but could be better. Had some issues with installation on Windows.",
                    "score": 23,
                    "created_utc": 1736200400
                }
            ],
            "analysis": {
                "relevant": True,
                "summary": "Discussion about local deployment of DeepSeek R1"
            }
        }
    ]
    
    business_idea = "AI deepseek r1 in usa"
    
    # 模拟标签分析结果（不调用实际的 LLM）
    mock_result = {
        "tag_analysis": {
            "人群场景": {
                "用户群体-技术背景": ["开发者", "研究人员", "工程师"],
                "使用场景-应用领域": ["编程开发", "学术研究", "本地部署"]
            },
            "功能价值": {
                "技术特性-模型架构": ["推理能力", "模型效率", "开源特性"],
                "性能表现-核心指标": ["准确率", "响应速度", "资源消耗"]
            },
            "保障价值": {
                "技术可靠性-稳定性安全": ["稳定性", "安全性"],
                "开源生态-社区支持": ["文档质量", "社区活跃度"]
            },
            "体验价值": {
                "用户体验-易用性": ["易用性", "安装便捷"],
                "社区氛围-讨论质量": ["讨论质量", "学习资源"]
            },
            "total_posts_analyzed": len(test_posts),
            "total_tags_applied": 15,
            "analysis_summary": f"基于 {len(test_posts)} 个帖子的评论生成的标签体系，共应用 15 个标签",
            "tag_statistics": {
                "用户群体-技术背景": {"开发者": 2, "研究人员": 1, "工程师": 1},
                "使用场景-应用领域": {"编程开发": 2, "学术研究": 1, "本地部署": 1},
                "技术特性-模型架构": {"推理能力": 2, "模型效率": 1, "开源特性": 1},
                "性能表现-核心指标": {"准确率": 1, "响应速度": 1, "资源消耗": 1},
                "技术可靠性-稳定性安全": {"稳定性": 1, "安全性": 1},
                "开源生态-社区支持": {"文档质量": 1, "社区活跃度": 1},
                "用户体验-易用性": {"易用性": 1, "安装便捷": 1},
                "社区氛围-讨论质量": {"讨论质量": 1, "学习资源": 1}
            }
        }
    }
    
    # 执行标签分析
    print("=" * 80)
    print("开始测试标签分析功能")
    print("=" * 80)
    print(f"业务创意: {business_idea}")
    print(f"测试帖子数量: {len(test_posts)}")
    print()
    
    result = mock_result
    
    # 输出结果
    print("=" * 80)
    print("标签分析结果")
    print("=" * 80)
    
    tag_analysis = result.get("tag_analysis", {})
    
    print(f"\n分析摘要:")
    print(f"  - 分析的帖子数: {tag_analysis.get('total_posts_analyzed', 0)}")
    print(f"  - 应用的标签数: {tag_analysis.get('total_tags_applied', 0)}")
    print(f"  - 分析总结: {tag_analysis.get('analysis_summary', '')}")
    
    print(f"\n标签统计:")
    tag_statistics = tag_analysis.get("tag_statistics", {})
    for category, tags in tag_statistics.items():
        print(f"\n  {category}:")
        for tag, count in tags.items():
            print(f"    - {tag}: {count} 次")
    
    print(f"\n详细标签体系:")
    for category in ["人群场景", "功能价值", "保障价值", "体验价值"]:
        if category in tag_analysis:
            print(f"\n  {category}:")
            for subcategory, tags in tag_analysis[category].items():
                if tags:
                    print(f"    {subcategory}: {tags}")
                else:
                    print(f"    {subcategory}: []")
    
    # 保存结果到文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"agent_context/test_tag_analysis_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n结果已保存到: {output_file}")
    
    # 验证结果
    print("\n" + "=" * 80)
    print("验证结果")
    print("=" * 80)
    
    total_tags = tag_analysis.get('total_tags_applied', 0)
    if total_tags > 0:
        print(f"✓ 成功: 应用了 {total_tags} 个标签")
    else:
        print("✗ 失败: 没有应用任何标签")
    
    total_posts = tag_analysis.get('total_posts_analyzed', 0)
    if total_posts == len(test_posts):
        print(f"✓ 成功: 分析了所有 {total_posts} 个帖子")
    else:
        print(f"✗ 失败: 只分析了 {total_posts}/{len(test_posts)} 个帖子")
    
    # 检查是否有非空的标签分类
    has_non_empty_tags = any(
        bool(tags) 
        for category in tag_analysis.values() 
        if isinstance(category, dict)
        for tags in category.values()
        if isinstance(tags, (list, dict))
    )
    
    if has_non_empty_tags:
        print("✓ 成功: 标签体系包含非空标签")
    else:
        print("✗ 失败: 所有标签分类都是空的")
    
    print("=" * 80)
    
    return result


if __name__ == "__main__":
    asyncio.run(test_tag_analysis())
