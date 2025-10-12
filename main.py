import os
import argparse
from dotenv import load_dotenv
from settings import Settings
import yaml


def export_envs(environment: str = "dev") -> None:
    load_dotenv(dotenv_path=f".env.{environment}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load environment variables from specified.env file."
    )
    parser.add_argument(
        "--environment",
        type=str,
        default="dev",
        help="The environment to load (dev, test, prod)",
    )
    args = parser.parse_args()

    export_envs(args.environment)

    with open("secrets.yaml", "r") as f:
        secrets = yaml.safe_load(f)
        for key, item in secrets.items():
            os.environ[key] = item

    settings = Settings()

    print("APP_NAME: ", settings.APP_NAME)
    print("ENVIRONMENT: ", settings.ENVIRONMENT)
    print("SECRET: ", settings.SECRET)
