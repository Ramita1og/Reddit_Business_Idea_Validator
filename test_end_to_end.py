"""
端到端测试脚本

测试完整的 Reddit 数据抓取和分析流程
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from agents.config import get_config
from agents.subagents.scraper_agent import ScraperAgent
from agents.context_store import ContextStore
from agents.skills.scraper_skills import (
    search_posts_skill,
    get_comments_skill,
    batch_get_comments_skill,
    batch_scrape_skill,
    batch_scrape_with_comments_skill
)
from mcp_servers.reddit_server import RedditMCPServer


async def test_search_posts():
    """测试搜索帖子功能"""
    print("\n" + "=" * 60)
    print("测试 1: 搜索帖子")
    print("=" * 60)

    # 加载配置
    config_manager = get_config()
    context_store = ContextStore()
    
    # 创建 Reddit MCP 服务器
    reddit_server = RedditMCPServer(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "BusinessResearchAgent/1.0 by test_user")
    )
    await reddit_server.start()
    
    agent = ScraperAgent(
        config=config_manager,
        context_store=context_store,
        mcp_clients={"reddit": reddit_server}
    )

    # 搜索帖子
    result = await search_posts_skill(
        agent,
        keyword="machine learning",
        sort="relevance",
        time_filter="all",
        limit=5
    )

    if result.get("success"):
        posts = result.get("posts", [])
        print(f"\n✅ 搜索成功! 找到 {len(posts)} 个帖子")
        
        for i, post in enumerate(posts[:3], 1):
            print(f"\n  [{i}] {post.get('title', 'N/A')}")
            print(f"      ID: {post.get('post_id')}")
            print(f"      子版块: {post.get('subreddit')}")
            print(f"      得分: {post.get('score')}")
            print(f"      评论数: {post.get('num_comments')}")
        
        await reddit_server.stop()
        return result
    else:
        print(f"\n❌ 搜索失败: {result.get('error')}")
        await reddit_server.stop()
        return None


async def test_get_comments(post_id: str):
    """测试获取评论功能"""
    print("\n" + "=" * 60)
    print("测试 2: 获取评论")
    print("=" * 60)

    # 加载配置
    config_manager = get_config()
    context_store = ContextStore()
    
    # 创建 Reddit MCP 服务器
    reddit_server = RedditMCPServer(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "BusinessResearchAgent/1.0 by test_user")
    )
    await reddit_server.start()
    
    agent = ScraperAgent(
        config=config_manager,
        context_store=context_store,
        mcp_clients={"reddit": reddit_server}
    )

    # 获取评论
    result = await get_comments_skill(
        agent,
        post_id=post_id,
        limit=5
    )

    if result.get("success"):
        comments = result.get("comments", [])
        print(f"\n✅ 获取评论成功! 找到 {len(comments)} 条评论")
        
        for i, comment in enumerate(comments[:3], 1):
            print(f"\n  [{i}] {comment.get('body', 'N/A')[:80]}...")
            print(f"      作者: {comment.get('author')}")
            print(f"      得分: {comment.get('score')}")
        
        await reddit_server.stop()
        return result
    else:
        print(f"\n❌ 获取评论失败: {result.get('error')}")
        await reddit_server.stop()
        return None


async def test_batch_get_comments(post_ids: list):
    """测试批量获取评论功能"""
    print("\n" + "=" * 60)
    print("测试 3: 批量获取评论")
    print("=" * 60)

    # 加载配置
    config_manager = get_config()
    context_store = ContextStore()
    
    # 创建 Reddit MCP 服务器
    reddit_server = RedditMCPServer(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "BusinessResearchAgent/1.0 by test_user")
    )
    await reddit_server.start()
    
    agent = ScraperAgent(
        config=config_manager,
        context_store=context_store,
        mcp_clients={"reddit": reddit_server}
    )

    # 批量获取评论
    result = await batch_get_comments_skill(
        agent,
        post_ids=post_ids,
        comments_per_post=3
    )

    if result.get("success"):
        results = result.get("results", {})
        total_comments = result.get("total_comments", 0)
        print(f"\n✅ 批量获取评论成功!")
        print(f"  处理的帖子数: {len(results)}")
        print(f"  总评论数: {total_comments}")
        
        for post_id, comments in results.items():
            print(f"\n  帖子 {post_id}: {len(comments)} 条评论")
        
        await reddit_server.stop()
        return result
    else:
        print(f"\n❌ 批量获取评论失败: {result.get('error')}")
        await reddit_server.stop()
        return None


async def test_batch_scrape():
    """测试批量抓取功能"""
    print("\n" + "=" * 60)
    print("测试 4: 批量抓取")
    print("=" * 60)

    # 加载配置
    config_manager = get_config()
    context_store = ContextStore()
    
    # 创建 Reddit MCP 服务器
    reddit_server = RedditMCPServer(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "BusinessResearchAgent/1.0 by test_user")
    )
    await reddit_server.start()
    
    agent = ScraperAgent(
        config=config_manager,
        context_store=context_store,
        mcp_clients={"reddit": reddit_server}
    )

    # 批量抓取
    result = await batch_scrape_skill(
        agent,
        keywords=["AI", "machine learning"],
        max_posts=3,
        comments_per_post=5
    )

    if result.get("success"):
        posts = result.get("posts", [])
        comments = result.get("comments", {})
        total_posts = result.get("total_posts", 0)
        total_comments = result.get("total_comments", 0)
        
        print(f"\n✅ 批量抓取成功!")
        print(f"  总帖子数: {total_posts}")
        print(f"  总评论数: {total_comments}")
        print(f"  执行时间: {result.get('execution_time', 0):.2f}秒")
        
        keyword_results = result.get("keyword_results", {})
        for keyword, stats in keyword_results.items():
            print(f"\n  关键词 '{keyword}':")
            print(f"    帖子数: {stats.get('posts_count', 0)}")
            print(f"    评论数: {stats.get('comments_count', 0)}")
        
        await reddit_server.stop()
        return result
    else:
        print(f"\n❌ 批量抓取失败: {result.get('error')}")
        await reddit_server.stop()
        return None


async def test_batch_scrape_with_comments():
    """测试批量抓取并合并评论功能"""
    print("\n" + "=" * 60)
    print("测试 5: 批量抓取并合并评论")
    print("=" * 60)

    # 加载配置
    config_manager = get_config()
    context_store = ContextStore()
    
    # 创建 Reddit MCP 服务器
    reddit_server = RedditMCPServer(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "BusinessResearchAgent/1.0 by test_user")
    )
    await reddit_server.start()
    
    agent = ScraperAgent(
        config=config_manager,
        context_store=context_store,
        mcp_clients={"reddit": reddit_server}
    )

    # 批量抓取并合并评论
    result = await batch_scrape_with_comments_skill(
        agent,
        keywords=["AI"],
        max_posts=3,
        comments_per_post=5
    )

    if result.get("success"):
        posts_with_comments = result.get("posts_with_comments", [])
        metadata = result.get("metadata", {})
        
        print(f"\n✅ 批量抓取并合并评论成功!")
        print(f"  总帖子数: {metadata.get('total_posts', 0)}")
        print(f"  有评论的帖子: {metadata.get('posts_with_comments', 0)}")
        print(f"  无评论的帖子: {metadata.get('posts_without_comments', 0)}")
        print(f"  总评论数: {metadata.get('total_comments', 0)}")
        
        for i, post in enumerate(posts_with_comments[:2], 1):
            print(f"\n  [{i}] {post.get('title', 'N/A')[:50]}...")
            print(f"      帖子ID: {post.get('post_id')}")
            print(f"      评论数: {len(post.get('comments_data', []))}")
        
        await reddit_server.stop()
        return result
    else:
        print(f"\n❌ 批量抓取并合并评论失败: {result.get('error')}")
        await reddit_server.stop()
        return None


async def main():
    """主函数"""
    print("=" * 60)
    print("Reddit 业务调研系统 - 端到端测试")
    print("=" * 60)

    load_dotenv()

    # 检查 Reddit 凭证
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("\n❌ 错误: 缺少 Reddit 凭证")
        print("请在 .env 文件中设置 REDDIT_CLIENT_ID 和 REDDIT_CLIENT_SECRET")
        return False

    if client_id.startswith("your_reddit") or client_secret.startswith("your_reddit"):
        print("\n❌ 错误: 检测到占位符凭证")
        print("请在 .env 文件中配置真实的 Reddit API 凭证")
        return False

    all_passed = True

    # 测试 1: 搜索帖子
    search_result = await test_search_posts()
    if not search_result:
        all_passed = False

    # 测试 2: 获取评论
    if search_result and search_result.get("posts"):
        post_id = search_result["posts"][0].get("post_id")
        comments_result = await test_get_comments(post_id)
        if not comments_result:
            all_passed = False

    # 测试 3: 批量获取评论
    if search_result and len(search_result.get("posts", [])) >= 2:
        post_ids = [p.get("post_id") for p in search_result["posts"][:2]]
        batch_comments_result = await test_batch_get_comments(post_ids)
        if not batch_comments_result:
            all_passed = False

    # 测试 4: 批量抓取
    batch_scrape_result = await test_batch_scrape()
    if not batch_scrape_result:
        all_passed = False

    # 测试 5: 批量抓取并合并评论
    batch_scrape_with_comments_result = await test_batch_scrape_with_comments()
    if not batch_scrape_with_comments_result:
        all_passed = False

    # 总结
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有端到端测试通过!")
        print("=" * 60)
        print("\n🎉 Reddit 业务调研系统已成功部署并测试!")
        print("系统已准备好进行 Reddit 数据抓取和分析。")
        return True
    else:
        print("❌ 部分测试失败")
        print("=" * 60)
        print("\n请检查错误信息并修复问题。")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
