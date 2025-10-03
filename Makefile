uv:
	pip install --upgrade pip && pip install uv
server:
	uv run mcp_server.py
client:
	uv run mcp_client.py
git:
	git add .
	git status
	git commit -m "recent edits"
	git push

format:
	python3 -m black . --include '\.py'
