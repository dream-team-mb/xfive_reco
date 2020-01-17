import importlib
import os


stage = os.environ.get('STAGE', 'not_specified')
if stage == 'not_specified':  # pragma: no cover
    pass
else:
    pass

modules = ['base', stage]

for module in modules:
    try:
        local_settings = importlib.import_module(f'config.{module}')
        globals().update(local_settings.__dict__)
    except ImportError:
        print(f'Failed to import config.{module}')    # noqa
    else:
        if os.environ.get('DEBUG_SETTINGS'):
            print(f'Imported config.{module}')    # noqa
