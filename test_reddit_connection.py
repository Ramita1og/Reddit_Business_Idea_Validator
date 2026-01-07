"""
Reddit MCP 服务器测试脚本

测试 Reddit API 连接和基本功能
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from mcp_servers.reddit_server import PRAWRedditClient, RedditMCPServer


async def test_reddit_connection():
    """测试 Reddit API 连接"""
    print("=" * 60)
    print("Reddit MCP 服务器连接测试")
    print("=" * 60)

    # 加载环境变量
    load_dotenv()

    # 获取 Reddit 凭证
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT", "BusinessResearchAgent/1.0 by test_user")

    # 检查凭证
    if not client_id or not client_secret:
        print("\n❌ 错误: 缺少 Reddit 凭证")
        print("请在 .env 文件中设置以下环境变量:")
        print("  - REDDIT_CLIENT_ID")
        print("  - REDDIT_CLIENT_SECRET")
        print("  - REDDIT_USER_AGENT")
        print("\n获取方式: https://www.reddit.com/prefs/apps")
        return False

    # 检查是否为占位符
    if client_id.startswith("your_reddit") or client_secret.startswith("your_reddit"):
        print("\n⚠️  检测到占位符凭证")
        print("\n📋 如何获取 Reddit API 凭证:")
        print("\n步骤 1: 登录 Reddit 账号")
        print("  访问: https://www.reddit.com")
        
        print("\n步骤 2: 创建应用")
        print("  访问: https://www.reddit.com/prefs/apps")
        print("  点击 'create another app...' 或 'create app'")
        
        print("\n步骤 3: 填写应用信息")
        print("  - name: 应用名称（例如: BusinessResearchAgent）")
        print("  - type: 选择 'script'")
        print("  - description: 应用描述")
        print("  - about url: 可以留空或填入你的网站")
        print("  - redirect uri: 填入 http://localhost:8080")
        
        print("\n步骤 4: 获取凭证")
        print("  - client_id: 应用ID（14字符的字符串）")
        print("  - client_secret: 应用密钥")
        
        print("\n步骤 5: 配置 .env 文件")
        print("  REDDIT_CLIENT_ID=\"你的client_id\"")
        print("  REDDIT_CLIENT_SECRET=\"你的client_secret\"")
        print("  REDDIT_USER_AGENT=\"BusinessResearchAgent/1.0 by 你的Reddit用户名\"")
        
        print("\n📖 更多信息:")
        print("  - PRAW 文档: https://praw.readthedocs.io/")
        print("  - Reddit API 文档: https://www.reddit.com/dev/api/")
        
        return False

    print(f"\n📝 凭证信息:")
    print(f"  Client ID: {client_id[:10]}...")
    print(f"  Client Secret: {client_secret[:10]}...")
    print(f"  User Agent: {user_agent}")

    try:
        # 创建 Reddit MCP 服务器
        print("\n🔗 正在连接 Reddit API...")
        server = RedditMCPServer(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        await server.start()
        print("✅ Reddit MCP 服务器创建成功")

        # 测试 1: 搜索帖子
        print("\n" + "=" * 60)
        print("测试 1: 搜索帖子")
        print("=" * 60)
        
        query = "AI"
        print(f"\n🔍 搜索关键词: '{query}'")
        print("排序方式: relevance")
        print("时间范围: all")
        print("返回数量: 5")
        
        search_result = await server.search_posts(
            keyword=query,
            sort="relevance",
            time_filter="all",
            limit=5
        )
        
        if search_result.get("success"):
            posts = search_result.get("posts", [])
            print(f"\n✅ 搜索成功! 找到 {len(posts)} 个帖子")
            
            if posts:
                print("\n前 3 个帖子:")
                for i, post in enumerate(posts[:3], 1):
                    print(f"\n  [{i}] {post.get('title', 'N/A')}")
                    print(f"      ID: {post.get('post_id', 'N/A')}")
                    print(f"      作者: {post.get('author', 'N/A')}")
                    print(f"      子版块: {post.get('subreddit', 'N/A')}")
                    print(f"      得分: {post.get('score', 0)}")
                    print(f"      评论数: {post.get('num_comments', 0)}")
                    print(f"      URL: {post.get('url', 'N/A')}")
        else:
            print(f"\n❌ 搜索失败: {search_result.get('error')}")
            await server.stop()
            return False

        # 测试 2: 获取评论
        print("\n" + "=" * 60)
        print("测试 2: 获取帖子评论")
        print("=" * 60)
        
        if posts:
            post_id = posts[0].get('post_id')
            print(f"\n📝 帖子 ID: {post_id}")
            print("获取评论数: 10")
            
            comments_result = await server.get_post_comments(
                post_id=post_id,
                limit=10
            )
            
            if comments_result.get("success"):
                comments = comments_result.get("comments", [])
                print(f"\n✅ 获取评论成功! 找到 {len(comments)} 条评论")
                
                if comments:
                    print("\n前 5 条评论:")
                    for i, comment in enumerate(comments[:5], 1):
                        print(f"\n  [{i}] {comment.get('body', 'N/A')[:100]}...")
                        print(f"      ID: {comment.get('comment_id', 'N/A')}")
                        print(f"      作者: {comment.get('author', 'N/A')}")
                        print(f"      得分: {comment.get('score', 0)}")
                        print(f"      深度: {comment.get('depth', 0)}")
            else:
                print(f"\n❌ 获取评论失败: {comments_result.get('error')}")
        else:
            print("\n⚠️  跳过评论测试: 没有可用的帖子")

        # 测试 3: 批量获取评论
        print("\n" + "=" * 60)
        print("测试 3: 批量获取评论")
        print("=" * 60)
        
        if len(posts) >= 2:
            post_ids = [p.get('post_id') for p in posts[:2]]
            print(f"\n📝 帖子 ID 列表: {post_ids}")
            print("每个帖子评论数: 5")
            
            batch_result = await server.batch_get_comments(
                post_ids=post_ids,
                comments_per_post=5
            )
            
            if batch_result.get("success"):
                results = batch_result.get("results", {})
                print(f"\n✅ 批量获取评论成功!")
                print(f"  处理的帖子数: {len(results)}")
                total_comments = sum(len(comments) for comments in results.values())
                print(f"  总评论数: {total_comments}")
                
                for post_id, comments in results.items():
                    print(f"\n  帖子 {post_id}: {len(comments)} 条评论")
            else:
                print(f"\n❌ 批量获取评论失败: {batch_result.get('error')}")
        else:
            print("\n⚠️  跳过批量评论测试: 帖子数量不足")

        # 停止服务器
        await server.stop()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主函数"""
    success = await test_reddit_connection()
    
    if success:
        print("\n🎉 Reddit API 连接测试成功!")
        print("系统已准备好使用 Reddit 数据抓取功能。")
        sys.exit(0)
    else:
        print("\n❌ Reddit API 连接测试失败!")
        print("请检查凭证配置和网络连接。")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
