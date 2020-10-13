import pytest

from poetry_poems.environment import EnvVars


def test_env_vars_ok(TempEnviron):
    with TempEnviron():
        env_vars = EnvVars()
    error = env_vars.validate_environment()
    assert error is None


@pytest.mark.parametrize("env_var, error_msg", [
    ('POETRY_ACTIVE', 'Poetry Shell is already active'),
    ('PIPENV_ACTIVE', 'Pipenv Shell is already active'),
    ('VENV', 'Virtual environment is already active'),
    ('VIRTUAL_ENV', 'Virtual environment is already active'),
])
def test_env_vars_errors(env_var, error_msg, TempEnviron):
    env = {env_var: '1'}
    with TempEnviron(**env):
        env_vars = EnvVars()
    result = env_vars.validate_environment()
    assert error_msg in result
