# base
from argparse import ArgumentParser
from os import system as run_shell_command

# application setup
from toolbox import create_app

def parse_args():
    parser = ArgumentParser(description="VEDB Toolbox application setup.")
    
    # Add a command-line argument for the config type
    parser.add_argument(
        "--config",
        choices = ["development", "debug", "production"],
        default = "development",
        help = "Specify the configuration to use: 'development' (default), 'debug', or 'production'."
    )
    
    return parser.parse_args()

def run_app(config_type):
    #Run the Flask app based on the provided configuration type

    if config_type == "debug":
        app = create_app(test_config=True)
        app.run(debug=True)
    elif config_type == "production":
        # Production deployment with Gunicorn
        run_shell_command("gunicorn --workers=2 'toolbox:create_app(test_config=None)'")
    else:
        # Default to development configuration
        app = create_app(test_config=None)
        app.run()

if __name__ == "__main__":
    # Run the app based on the selected configuration parsed from the command line
    run_app(parse_args().config)