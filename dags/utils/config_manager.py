from json import JSONDecodeError
from pathlib import Path

import yaml
from airflow.models import Variable


class ConfigManager:
    def __init__(self):
        super().__init__()

    def load_config(self, env: str):
        print('Loading config for environment : ', env)
        config_path = Path(__file__).parents[1] / "config" / f"{env}.yaml"
        config = self._load_yaml(config_path)
        config = self._update_config_with_variables(config, env)
        return config

    def _load_yaml(self, path: Path):
        with open(path) as f:
            return yaml.safe_load(f)

    def _get_variable(self, var_name: str, default_value):
        """Retrieve Airflow Variable """
        if Variable.get(var_name, None) is None:
            return default_value
        try:
            return Variable.get(var_name, default_var=default_value, deserialize_json=True)
        except JSONDecodeError:
            return Variable.get(var_name, default_var=default_value, deserialize_json=False)

    def _update_config_with_variables(self, config: dict, env: str, parent_key: str = "") -> dict:
        """Recursively walk through nested config and override with Airflow Variables."""
        updated = {}
        for key, value in config.items():
            full_key = f"{parent_key}_{key}" if parent_key else key
            var_name = f"{env}_{full_key}"
            if isinstance(value, dict):
                updated[key] = self._update_config_with_variables(value, env, full_key)
            else:
                updated[key] = self._get_variable(var_name, value)
        return updated
