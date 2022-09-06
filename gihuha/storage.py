from diskcache import Cache

storage = Cache(
    "./storage",
    size_limit=1e32,
    disk_min_file_size=1048576,
)
