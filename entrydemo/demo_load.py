from importlib.metadata import entry_points

def main(group_name):
    print(f"加载插件组：{group_name}...")
    eps = entry_points().select(group=group_name)
    for ep in eps:
        print(f"发现插件: {ep.name} -> {ep.value}")
        cls = ep.load()
        obj = cls()
        ok = obj.authenticate("admin", "secret")
        print(f"认证结果 {ok}")

if __name__ == "__main__":
    main("auth.plugins")
