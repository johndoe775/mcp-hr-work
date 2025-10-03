uv:
	pip install --upgrade pip && pip install uv
	
git:
	git add .
	git status
	git commit -m "recent edits"
	git push

format:
	python3 -m black . --include '\.py'
