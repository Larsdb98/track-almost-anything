from track_almost_anything.cli import app_parser
from track_almost_anything._logging import configure_logger, log_info, log_error


def main() -> int:
    args = app_parser()
    log_level = args.log_level
    log_dir = args.log_dir

    configure_logger(log_level=log_level, log_dir=log_dir)
    log_info("_______________ Track Almost Anything _______________")
    log_info("App launched !")

    return 0


if __name__ == "__main__":
    main()
