# Reddit_Business_Idea_Validator - Qwen Code Context

## Project Overview

This is a multi-agent system for business idea validation that collects and analyzes data from social media platforms, primarily Reddit, to analyze market demand, user pain points, and competitive landscape. The system uses AI and web scraping to provide comprehensive market validation reports.

**Note**: The project contains both Reddit and Xiaohongshu (XHS/Red) integration code, but the README and primary focus is on Reddit. The system is designed to be platform-agnostic with a modular architecture.

### Architecture

The system follows a modular multi-agent architecture with the following key components:

1. **Agents**: Core intelligence units that perform specific tasks
2. **MCP Servers**: Microservice-based servers for different capabilities
3. **Context Store**: Shared state management between agents
4. **Models**: Data structures and business logic models
5. **Config**: Configuration management system

### Core Components

#### 1. Base Agent (`agents/base_agent.py`)
- Abstract base class for all agents
- Provides unified interfaces for MCP calls, LLM interactions, and progress tracking
- Implements lifecycle management (start, stop, pause, resume)
- Includes metrics tracking and checkpoint management

#### 2. Context Store (`agents/context_store.py`)
- Centralized storage for shared context between agents
- Manages run contexts, progress tracking, and agent states
- Supports both in-memory and file-based persistence
- Implements TTL-based cleanup for expired data

#### 3. Configuration Manager (`agents/config.py`)
- Handles configuration loading from YAML, JSON, and environment variables
- Supports different configuration types (Reddit, LLM, Storage, Orchestrator)
- Provides default values and environment variable overrides

#### 4. MCP Servers (`mcp_servers/`)
- **Reddit Server**: Interfaces with Reddit API using PRAW for data
- **XHS Server**: Interfaces with TikHub API for Xiaohongshu data
- **LLM Server**: Provides LLM capabilities for analysis and generation
- **Storage Server**: Manages checkpoint persistence and data storage

#### 5. Models (`models/`)
- **Agent Models**: Task results, progress updates, execution plans
- **Context Models**: Run contexts, agent states
- **Business Models**: Reddit posts, comments, analysis results

## Building and Running

### Prerequisites
- Python 3.9+
- Reddit API credentials (client ID, client secret, user agent)
- LLM API key (OpenAI, etc.)

### Setup
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables by copying `.env.example` to `.env`:
   ```bash
   # Copy the example configuration
   copy .env.example .env
   ```
   
3. Edit the `.env` file to add your API keys:
   - `REDDIT_CLIENT_ID`: Your Reddit app client ID
   - `REDDIT_CLIENT_SECRET`: Your Reddit app client secret
   - `REDDIT_USER_AGENT`: Your Reddit user agent string
   - `OPENAI_API_KEY`: Your OpenAI API key (or equivalent)
   - `OPENAI_BASE_URL`: API endpoint URL

### Running the System
Execute the main validation script:
```bash
python run_agent.py "Your business idea here"
```

Or run interactively:
```bash
python run_agent.py
# Then enter your business idea when prompted
```

For faster execution, you can use fast mode by responding 'y' when prompted.

### Running Tests
Execute the integration tests to verify system functionality:
```bash
python test_reddit_connection.py
python test_end_to_end.py
```

### Main Execution Flow
The orchestrator agent manages the complete business validation workflow:
1. **Keyword Generation**: Generate relevant search keywords (or use user input directly)
2. **Data Scraping**: Collect Reddit posts and comments
3. **Data Analysis**: Analyze content for market signals and user pain points
4. **Report Generation**: Create comprehensive validation report

## Development Conventions

### Code Structure
- All agents inherit from `BaseAgent`
- MCP servers follow a consistent interface pattern with `call_tool` method
- Models use Pydantic for data validation
- Async/await patterns for I/O operations
- Thread-safe context store operations

### Error Handling
- Comprehensive exception handling with logging
- Retry mechanisms with exponential backoff
- Graceful degradation when services are unavailable

### Configuration
- Centralized configuration management
- Environment variable overrides
- YAML/JSON configuration file support
- Default values for all settings

### Testing
- Integration tests verify end-to-end functionality
- Tests cover MCP servers, context store, and configuration
- Mock-friendly architecture for unit testing

## Key Features

### 1. Multi-Agent Architecture
- Orchestrator coordinates the validation workflow
- Specialized agents for different tasks (keyword generation, scraping, analysis, reporting)
- Agent delegation and communication mechanisms

### 2. MCP (Microservice Control Protocol)
- Standardized interface for different service types
- Pluggable architecture for adding new capabilities
- Centralized service management

### 3. Progress Tracking
- Real-time progress updates during execution
- Detailed progress history and metrics
- Callback mechanisms for external progress monitoring

### 4. Checkpoint Management
- Save/restore functionality for long-running processes
- Automatic checkpointing at defined intervals
- Resume from failure capabilities

### 5. Data Models
- Rich data models for Reddit content
- Comprehensive analysis results structure
- Validation result aggregation

## Available Skills

The system includes a comprehensive set of skills organized by functional areas:

### Scraper Skills
- `search_posts_skill`: Search Reddit posts by keyword
- `get_comments_skill`: Get comments for a specific post
- `batch_get_comments_skill`: Get comments for multiple posts in batch
- `batch_scrape_skill`: Perform batch scraping of posts and comments
- `batch_scrape_with_comments_skill`: Batch scraping with comments merged to posts

### Analyzer Skills
- `analyze_post_skill`: Analyze individual posts for relevance and insights
- `analyze_comments_skill`: Analyze comments for user sentiment and themes
- `batch_analyze_posts_skill`: Batch analysis of multiple posts
- `generate_combined_analysis_skill`: Generate comprehensive market analysis

### Reporter Skills
- `generate_text_report_skill`: Create text format validation reports
- `generate_html_report_skill`: Create HTML format validation reports with styling
- `save_report_skill`: Save reports to file system

## File Structure
```
reddit_business_agent/
├── models/                 # Data models
│   ├── __init__.py
│   ├── agent_models.py     # Agent-related models
│   ├── context_models.py   # Context models
│   └── business_models.py  # Business domain models
├── agents/                 # Agent implementations
│   ├── __init__.py
│   ├── base_agent.py       # Base agent class
│   ├── config.py           # Configuration management
│   ├── context_store.py    # Shared context management
│   ├── orchestrator.py     # Main orchestrator agent
│   ├── subagents/          # Specialized agents
│   │   ├── __init__.py
│   │   ├── scraper_agent.py    # Data scraping agent
│   │   ├── analyzer_agent.py   # Data analysis agent
│   │   └── reporter_agent.py   # Report generation agent
│   └── skills/             # Agent capabilities
│       ├── __init__.py
│       ├── scraper_skills.py
│       ├── analyzer_skills.py
│       └── reporter_skills.py
├── mcp_servers/            # MCP server implementations
│   ├── __init__.py
│   ├── reddit_server.py    # Reddit server
│   ├── xhs_server.py       # Xiaohongshu server
│   ├── llm_server.py       # LLM server
│   └── storage_server.py   # Storage server
├── tests/                  # Test files
│   ├── __init__.py
│   ├── test_integration.py # Integration tests
│   └── test_e2e.py         # End-to-end tests
├── reports/                # Generated reports
├── agent_context/          # Runtime context storage
│   └── checkpoints/        # Checkpoint files
├── requirements.txt        # Dependencies
├── run_agent.py            # Main execution script
├── test_reddit_connection.py # Reddit API connection test
├── test_end_to_end.py      # End-to-end test
├── README.md               # Project documentation
├── .env.example           # Environment variables example
└── .env                   # Environment variables (not in repo)
```

## Environment Variables
- `REDDIT_CLIENT_ID`: Reddit API client ID
- `REDDIT_CLIENT_SECRET`: Reddit API client secret
- `REDDIT_USER_AGENT`: Reddit user agent string
- `OPENAI_API_KEY`: API key for LLM service
- `OPENAI_BASE_URL`: Base URL for LLM API (default: OpenAI)
- `SCRAPER_PAGES_PER_KEYWORD`: Number of pages to scrape per keyword (default: 2)
- `SCRAPER_COMMENTS_PER_NOTE`: Number of comments to fetch per note (default: 20)
- `ANALYZER_MAX_POSTS`: Maximum number of posts to analyze (default: 20)
- `REPORT_OUTPUT_DIR`: Directory for generated reports (default: reports)

## API Integration
The system integrates with:
- Reddit API via PRAW for Reddit data access
- LLM APIs (OpenAI, etc.) for analysis and generation
- TikHub API for Xiaohongshu data access (dual platform support)
- File system or Redis for persistent storage

## Development Notes
- The system is designed to be extensible for additional social media platforms
- Error handling and retry mechanisms are built into the base agent class
- Fast mode is available for quicker validation with reduced data collection
- The system supports checkpointing to resume from failures
- The system uses a unified data model (`PostWithComments`) that works with both Reddit and Xiaohongshu data
- The orchestrator now skips keyword generation and directly uses user input as the search keyword
- The system includes advanced comment analysis with tag system based on functions.txt