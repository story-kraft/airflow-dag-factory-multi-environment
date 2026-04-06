
def register_dag(dag_name, create_dag_fn, load_config_fn):
    for env in ["dev", "test", "prod"]:
        dag_id = f"{dag_name}_{env}"
        config = load_config_fn(env)
        config["env"] = env
        globals()[dag_id] = create_dag_fn(dag_id, config)

