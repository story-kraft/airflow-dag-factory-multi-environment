import copy

def register_dag(dag_name, create_dag_fn, load_config_fn):
    # Env can be externalized
    for env in ["dev", "test", "prod"]:
        dag_id = f"{dag_name}_{env}"
        config = copy.deepcopy(load_config_fn(env))
        config["env"] = env
        globals()[dag_id] = create_dag_fn(dag_id, config)

