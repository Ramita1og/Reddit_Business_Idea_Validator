"""
Reddit MCP 服务器

基于 PRAW（Python Reddit API Wrapper）提供 Reddit 数据获取服务
"""

import praw
import logging
import time
from typing import Dict, Any, List, Optional
from datetime import datetime

from models.business_models import RedditPostModel, RedditCommentModel
from agents.logging_config import RequestLogger


logger = logging.getLogger("mcp.reddit_server")


# ============================================================================
# PRAW Reddit Client
# ============================================================================

class PRAWRedditClient:
    """
    PRAW Reddit 客户端
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str
    ):
        """
        初始化客户端

        Args:
            client_id: Reddit应用客户端ID
            client_secret: Reddit应用客户端密钥
            user_agent: 用户代理字符串
        """
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        self.request_logger = RequestLogger(logger)

    def search_submissions(
        self,
        query: str,
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 100,
        subreddit: Optional[str] = None
    ) -> List[Any]:
        """
        搜索Reddit帖子

        Args:
            query: 搜索关键词
            sort: 排序方式 (relevance/hot/top/new/comments)
            time_filter: 时间范围 (all/hour/day/week/month/year)
            limit: 返回结果数量
            subreddit: 子版块名称（None表示全站搜索）

        Returns:
            submission对象列表
        """
        # 记录请求日志
        self.request_logger.log_request(
            api_name="PRAW.Reddit",
            method="search",
            url=f"search?query={query}",
            params={"sort": sort, "time_filter": time_filter, "limit": limit}
        )

        start_time = time.time()

        try:
            if subreddit:
                search_results = self.reddit.subreddit(subreddit).search(
                    query=query,
                    sort=sort,
                    time_filter=time_filter,
                    limit=limit
                )
            else:
                search_results = self.reddit.subreddit("all").search(
                    query=query,
                    sort=sort,
                    time_filter=time_filter,
                    limit=limit
                )

            submissions = list(search_results)
            duration_ms = (time.time() - start_time) * 1000

            # 记录响应日志
            self.request_logger.log_response(
                api_name="PRAW.Reddit",
                status=200,
                body={"submissions_count": len(submissions), "query": query},
                duration_ms=duration_ms
            )

            return submissions

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.request_logger.log_response(
                api_name="PRAW.Reddit",
                error=str(e),
                duration_ms=duration_ms
            )
            raise

    def get_submission_comments(
        self,
        submission_id: str,
        limit: int = 50
    ) -> List[Any]:
        """
        获取帖子的评论

        Args:
            submission_id: 帖子ID
            limit: 最大评论数

        Returns:
            comment对象列表
        """
        # 记录请求日志
        self.request_logger.log_request(
            api_name="PRAW.Reddit",
            method="get_comments",
            url=f"submission/{submission_id}/comments",
            params={"limit": limit}
        )

        start_time = time.time()

        try:
            submission = self.reddit.submission(id=submission_id)
            submission.comments.replace_more(limit=None)  # 展开所有评论

            comments = submission.comments.list()[:limit]
            duration_ms = (time.time() - start_time) * 1000

            # 记录响应日志
            self.request_logger.log_response(
                api_name="PRAW.Reddit",
                status=200,
                body={"comments_count": len(comments), "submission_id": submission_id},
                duration_ms=duration_ms
            )

            return comments

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.request_logger.log_response(
                api_name="PRAW.Reddit",
                error=str(e),
                duration_ms=duration_ms
            )
            raise


# ============================================================================
# Reddit MCP Server
# ============================================================================


class RedditMCPServer:
    """
    Reddit MCP 服务器

    提供工具:
    - search_posts: 搜索帖子
    - get_post_comments: 获取评论
    - batch_get_comments: 批量获取评论
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        request_delay: float = 1.0
    ):
        """
        初始化 Reddit MCP 服务器

        Args:
            client_id: Reddit应用客户端ID
            client_secret: Reddit应用客户端密钥
            user_agent: 用户代理字符串
            request_delay: 请求延迟(秒)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.request_delay = request_delay
        self._client = None

        logger.info("Reddit MCP Server initialized")

    async def start(self):
        """启动服务器"""
        self._client = PRAWRedditClient(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent
        )
        logger.info("Reddit MCP Server started")

    async def stop(self):
        """停止服务器"""
        self._client = None
        logger.info("Reddit MCP Server stopped")

    # ========================================================================
    # MCP 工具实现
    # ========================================================================

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        调用工具

        Args:
            tool_name: 工具名称
            **kwargs: 工具参数

        Returns:
            工具执行结果
        """
        if tool_name == "search_posts":
            return await self.search_posts(**kwargs)
        elif tool_name == "get_post_comments":
            return await self.get_post_comments(**kwargs)
        elif tool_name == "batch_get_comments":
            return await self.batch_get_comments(**kwargs)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    async def search_posts(
        self,
        keyword: str,
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 100,
        subreddit: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        搜索Reddit帖子

        Args:
            keyword: 搜索关键词
            sort: 排序方式 (relevance/hot/top/new/comments)
            time_filter: 时间范围 (all/hour/day/week/month/year)
            limit: 返回结果数量
            subreddit: 子版块名称（None表示全站搜索）

        Returns:
            {
                "success": true,
                "keyword": "关键词",
                "posts": [帖子列表],
                "total_count": 帖子总数,
                "execution_time": 执行时间
            }
        """
        start_time = datetime.now()

        try:
            submissions = self._client.search_submissions(
                query=keyword,
                sort=sort,
                time_filter=time_filter,
                limit=limit,
                subreddit=subreddit
            )

            # 转换为模型
            posts = []
            for submission in submissions:
                post = RedditPostModel(
                    post_id=submission.id,
                    title=submission.title,
                    content=submission.selftext,
                    url=submission.url,
                    score=submission.score,
                    upvote_ratio=submission.upvote_ratio,
                    num_comments=submission.num_comments,
                    created_utc=int(submission.created_utc),
                    subreddit=submission.subreddit.display_name,
                    author=submission.author.name if submission.author else "[deleted]",
                    keyword_matched=keyword
                )
                posts.append(post.model_dump())

            execution_time = (datetime.now() - start_time).total_seconds()

            logger.info(f"Search complete: {len(posts)} posts in {execution_time:.2f}s")

            return {
                "success": True,
                "keyword": keyword,
                "posts": posts,
                "total_count": len(posts),
                "execution_time": execution_time
            }

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                "success": False,
                "keyword": keyword,
                "posts": [],
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def get_post_comments(
        self,
        post_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        获取帖子评论

        Args:
            post_id: 帖子 ID
            limit: 最大评论数

        Returns:
            {
                "success": true,
                "post_id": "帖子ID",
                "comments": [评论列表],
                "total_count": 评论总数,
                "execution_time": 执行时间
            }
        """
        start_time = datetime.now()

        try:
            comments = self._client.get_submission_comments(
                submission_id=post_id,
                limit=limit
            )

            # 转换为模型
            comment_list = []
            for comment in comments:
                if isinstance(comment, praw.models.Comment):
                    comment_model = RedditCommentModel(
                        comment_id=comment.id,
                        post_id=post_id,
                        body=comment.body,
                        score=comment.score,
                        created_utc=int(comment.created_utc),
                        author=comment.author.name if comment.author else "[deleted]",
                        parent_id=comment.parent_id,
                        depth=comment.depth
                    )
                    comment_list.append(comment_model.model_dump())

            execution_time = (datetime.now() - start_time).total_seconds()

            logger.info(f"Got {len(comment_list)} comments in {execution_time:.2f}s")

            return {
                "success": True,
                "post_id": post_id,
                "comments": comment_list,
                "total_count": len(comment_list),
                "execution_time": execution_time
            }

        except Exception as e:
            logger.error(f"Get comments failed: {e}")
            return {
                "success": False,
                "post_id": post_id,
                "comments": [],
                "error": str(e),
                "execution_time": (datetime.now() - start_time).total_seconds()
            }

    async def batch_get_comments(
        self,
        post_ids: List[str],
        comments_per_post: int = 20,
        delay_between_requests: float = 2.0
    ) -> Dict[str, Any]:
        """
        批量获取评论（串行以避免速率限制）

        Args:
            post_ids: 帖子 ID 列表
            comments_per_post: 每个帖子的评论数
            delay_between_requests: 请求之间的延迟（秒）

        Returns:
            {
                "success": true,
                "results": {post_id: [评论列表]},
                "total_comments": 总评论数,
                "execution_time": 执行时间
            }
        """
        import asyncio

        start_time = datetime.now()

        logger.info(f"Batch getting comments for {len(post_ids)} posts")

        results_dict = {}
        total_comments = 0

        for idx, post_id in enumerate(post_ids):
            try:
                # 添加延迟
                if idx > 0:
                    await asyncio.sleep(delay_between_requests)

                result = await self.get_post_comments(post_id, comments_per_post)

                if isinstance(result, dict) and result.get("success"):
                    comments = result.get("comments", [])
                    results_dict[post_id] = comments
                    total_comments += len(comments)
                    logger.info(f"Got {len(comments)} comments for post {post_id} ({idx + 1}/{len(post_ids)})")
                else:
                    logger.error(f"Failed to get comments for {post_id}: {result.get('error', 'Unknown error')}")
                    results_dict[post_id] = []

            except Exception as e:
                logger.error(f"Failed to get comments for {post_id}: {e}")
                results_dict[post_id] = []

        execution_time = (datetime.now() - start_time).total_seconds()

        logger.info(f"Batch complete: {total_comments} comments in {execution_time:.2f}s")

        return {
            "success": True,
            "results": results_dict,
            "total_comments": total_comments,
            "execution_time": execution_time
        }

    async def ping(self) -> bool:
        """健康检查"""
        return self._client is not None


# ============================================================================
# 服务器工厂
# ============================================================================

async def create_reddit_mcp_server(
    client_id: str,
    client_secret: str,
    user_agent: str,
    request_delay: float = 1.0
) -> RedditMCPServer:
    """
    创建 Reddit MCP 服务器实例

    Args:
        client_id: Reddit应用客户端ID
        client_secret: Reddit应用客户端密钥
        user_agent: 用户代理字符串
        request_delay: 请求延迟

    Returns:
        Reddit MCP 服务器实例
    """
    server = RedditMCPServer(client_id, client_secret, user_agent, request_delay)
    await server.start()
    return server
