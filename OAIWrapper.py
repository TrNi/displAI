"""OpenAI wrapper."""
import logging
import openai
import tiktoken
import yaml


# Set logging level
logging.basicConfig(level=logging.INFO)


class OAIWrapper():
    """OpenAI wrapper."""

    def __init__(self, config_file="config/config.yaml"):
        """Initialize the wrapper."""
        self.__last_response = None

        self.completion_config = {}
        self.chat_completion_config = {}
        self._load_config_from_file(config_file)
        self.completion_encoding = tiktoken.get_encoding(
            self.completion_config["encoding"]
        )
        self.chat_completion_encoding = tiktoken.get_encoding(
            self.chat_completion_config["encoding"]
        )

    def _load_config_from_file(self, config_file: str = "config/config.yaml"):
        """Load default config for completion and chatCompletion, from yaml files."""
        try:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
            self.completion_config = config["completion"]
            self.chat_completion_config = config["chatCompletion"]
        except Exception as e:
            logging.error("Error loading config file %s: %s", config_file, e)

    def _get_token_count(self, prompt: str, kind: str) -> int:
        """Returns the number of tokens in a text string."""
        if kind == "completion":
            n_tokens = self.completion_encoding.encode(prompt)
        elif kind == "chatCompletion":
            n_tokens = self.chat_completion_encoding.encode(prompt)
        logging.debug("tokens: (%s) %s", len(n_tokens), n_tokens)
        return len(n_tokens)

    def _call(self, prompt, kind: str = "completion", countTokens: bool = True) -> str:
        """Call the OpenAI API based on kind."""
        assert kind in ["completion", "chatCompletion"], f"Invalid kind: {kind}"

        if kind == "completion":
            kwargs = self.completion_config["kwargs"]
            kwargs["prompt"] = prompt
            method = openai.Completion.create
            max_tokens = self.completion_config["kwargs"]["max_tokens"]
        elif kind == "chatCompletion":
            kwargs = self.chat_completion_config["kwargs"]
            kwargs["messages"] = [{
                "role": "user",
                "content": prompt
            }]
            method = openai.ChatCompletion.create
            max_tokens = self.chat_completion_config["kwargs"]["max_tokens"]

        # Try to count tokens before calling the API
        try:
            if countTokens:
                tokens = self._get_token_count(prompt, kind)
                logging.info("Num tokens: %s", tokens)
                if tokens > max_tokens:
                    logging.error(f"Too many tokens: {tokens}")
                    return ""
        except Exception as e:
            logging.error("Count tokens error: %s", e)

        # Call the API
        try:
            resp = method(
                **kwargs
            )
            self.__last_response = resp
            logging.info("Usage: %s", resp.usage)
            logging.info("Finish reason: %s", resp.choices[0].finish_reason)
            return resp.choices[0].message["content"]
        except Exception as e:
            logging.error("Completion error: %s", e)

        return ""

    def chat_completion(self, prompt, countTokens: bool = True) -> str:
        """Call the OpenAI API for chatCompletion."""
        return self._call(
            prompt, kind="chatCompletion", countTokens=countTokens
        )

    def completion(self, prompt, countTokens: bool = True) -> str:
        """Call the OpenAI API for completion."""
        return self._call(
            prompt, kind="completion", countTokens=countTokens
        )

    def get_last_response(self) -> openai.Completion:
        """Get the last response (openai defined object) from the API."""
        return self.__last_response
