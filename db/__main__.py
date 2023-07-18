import argparse
import os
from pathlib import Path

from alembic.config import CommandLine, Config


def make_alembic_config(cmd_opts: argparse.Namespace) -> Config:
    """
    Создает объект конфигурации alembic на основе аргументов командной строки,
    подменяет относительные пути на абсолютные.
    """

    base_path = Path(__file__).parent.parent.resolve()

    # Подменяем путь до файла alembic.ini на абсолютный
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    # Подменяем путь до папки с alembic на абсолютный
    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))

    config.set_main_option('sqlalchemy.url', cmd_opts.db_url)

    return config


def main():
    alembic = CommandLine()

    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    alembic.parser.add_argument(
        '--db-url', default=None,
        help='Database URL',
        required=True
    )

    options = alembic.parser.parse_args()
    if 'cmd' not in options:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
