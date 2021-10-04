import envparse

env = envparse.Env()
env.read_envfile()

GITHUB_API_TOKEN = env.str("GITHUB_API_TOKEN", default=None)
