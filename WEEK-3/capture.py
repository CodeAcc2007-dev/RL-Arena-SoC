from collections import deque

def capture_territory(grid, player_id, rows, cols):
    """Flood fill from the grid border. Any cell NOT reachable from the
    border (without crossing player_id's trail/territory) is enclosed,
    and becomes player_id's territory."""

    def is_boundary(value):
        return abs(value) == player_id

    visited = [[False] * cols for _ in range(rows)]
    q = deque()

    for r in range(rows):
        for c in (0, cols - 1):
            if not is_boundary(grid[r, c]) and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))
    for c in range(cols):
        for r in (0, rows - 1):
            if not is_boundary(grid[r, c]) and not visited[r][c]:
                visited[r][c] = True
                q.append((r, c))

    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and not is_boundary(grid[nr, nc]):
                visited[nr][nc] = True
                q.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if not visited[r][c]:
                v = grid[r, c]
                if v == 0 or v == -player_id:
                    grid[r, c] = player_id
