"""Configuration for Matrix Webhook."""

import argparse
import os

parser = argparse.ArgumentParser(description=__doc__, prog="python -m matrix_webhook")
parser.add_argument(
    "-H",
    "--host",
    default=os.environ.get("HOST", ""),
    help="host to listen to. Default: `''`. Environment variable: `HOST`",
)
parser.add_argument(
    "-S",
    "--server-path",
    default=os.environ.get("SERVER_PATH", ""),
    help="unix path to listen to. Default: `''`. Environment variable: `SERVER_PATH`",
)
parser.add_argument(
    "-P",
    "--port",
    type=int,
    default=os.environ.get("PORT", 4785),
    help="port to listed to. Default: 4785. Environment variable: `PORT`",
)
parser.add_argument(
    "-u",
    "--matrix-url",
    default=os.environ.get("MATRIX_URL", "https://matrix.org"),
    help="matrix homeserver url. Default: `https://matrix.org`. "
    "Environment variable: `MATRIX_URL`",
)
parser.add_argument(
    "-i",
    "--matrix-id",
    help="matrix user-id. Required. Environment variable: `MATRIX_ID`",
    **(
        {"default": os.environ["MATRIX_ID"]}
        if "MATRIX_ID" in os.environ
        else {"required": True}
    ),
)
auth = parser.add_mutually_exclusive_group(
    required=all(v not in os.environ for v in ["MATRIX_PW", "MATRIX_PW_FILE", "MATRIX_TOKEN", "MATRIX_TOKEN_FILE"]),
)
auth.add_argument(
    "--matrix-pw",
    help="matrix password. Either this or token required. "
    "Environment variable: `MATRIX_PW`",
    **({"default": os.environ["MATRIX_PW"]} if "MATRIX_PW" in os.environ else {}),
)
auth.add_argument(
    "--matrix-pw-file",
    help="matrix password. Either this or token required. "
    "Environment variable: `MATRIX_PW_FILE`",
    **({"default": os.environ["MATRIX_PW_FILE"]} if "MATRIX_PW_FILE" in os.environ else {}),
)
auth.add_argument(
    "-t",
    "--matrix-token",
    help="matrix access token. Either this or password required. "
    "Environment variable: `MATRIX_TOKEN`",
    **({"default": os.environ["MATRIX_TOKEN"]} if "MATRIX_TOKEN" in os.environ else {}),
)
auth.add_argument(
    "--matrix-token-file",
    help="matrix access token. Either this or password required. "
    "Environment variable: `MATRIX_TOKEN_FILE`",
    **({"default": os.environ["MATRIX_TOKEN_FILE"]} if "MATRIX_TOKEN_FILE" in os.environ else {}),
)
key = parser.add_mutually_exclusive_group(
    required=all(v not in os.environ for v in ["API_KEY", "API_KEY_FILE"]),
)
key.add_argument(
    "-k",
    "--api-key",
    help="shared secret to use this service. Required. Environment variable: `API_KEY`",
    **(
        {"default": os.environ["API_KEY"]}
        if "API_KEY" in os.environ
        else {}
    ),
)
key.add_argument(
    "--api-key-file",
    help="shared secret to use this service. Required. Environment variable: `API_KEY_FILE`",
    **(
        {"default": os.environ["API_KEY_FILE"]}
        if "API_KEY_FILE" in os.environ
        else {}
    ),
)
parser.add_argument(
    "--https-proxy",
    help="https proxy to use. Environment variable: `https_proxy`",
    **(
        {"default": os.environ["https_proxy"]}
        if "https_proxy" in os.environ
        else {}
    ),
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=int(os.environ.get("VERBOSITY", 0)),
    help="increment verbosity level",
)

args = parser.parse_args()

SERVER_ADDRESS = (args.host, args.port)
SERVER_PATH = args.server_path
MATRIX_URL = args.matrix_url
MATRIX_ID = args.matrix_id

if args.matrix_pw_file:
    with open(args.matrix_pw_file, "r") as f:
        MATRIX_PW = f.read().strip()
else:
    MATRIX_PW = args.matrix_pw
if args.matrix_token_file:
    with open(args.matrix_token_file, "r") as f:
        MATRIX_TOKEN = f.read().strip()
else:
    MATRIX_TOKEN = args.matrix_token

if args.api_key_file:
    with open(args.api_key_file, "r") as f:
        API_KEY = f.read().strip()
else:
    API_KEY = args.api_key

VERBOSE = args.verbose
PROXY = args.https_proxy
