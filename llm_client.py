# import os
# from groq import Groq

# _client = None


# def _load_env():
#     """Load .env file manually — works even without python-dotenv installed."""
#     env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
#     if os.path.exists(env_path):
#         with open(env_path, "r") as f:
#             for line in f:
#                 line = line.strip()
#                 if line and not line.startswith("#") and "=" in line:
#                     key, _, value = line.partition("=")
#                     key = key.strip()
#                     value = value.strip().strip('"').strip("'")
#                     if key and value and key not in os.environ:
#                         os.environ[key] = value

# # def _load_env():
# #     """Load .env file manually — robust version."""
# #     env_path = os.path.join(
# #         os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
# #         ".env"
# #     )

# #     if os.path.exists(env_path):
# #         with open(env_path, "r") as f:
# #             for line in f:
# #                 line = line.strip()

# #                 # Skip empty lines and full-line comments
# #                 if not line or line.startswith("#"):
# #                     continue

# #                 if "=" in line:
# #                     key, _, value = line.partition("=")

# #                     key = key.strip()

# #                     # إزالة inline comments + تنظيف القيمة
# #                     value = value.split("#")[0].strip()
# #                     value = value.strip('"').strip("'")

# #                     if key and value:
# #                         # ✅ ALWAYS override existing env variables
# #                         os.environ[key] = value

#     # # 🔍 Debug print (remove after testing)
#     # print("Loaded GROQ_API_KEY:", repr(os.environ.get("GROQ_API_KEY")))

# def get_client() -> Groq:
#     global _client
#     if _client is None:
#         _load_env()
#         api_key = os.environ.get("GROQ_API_KEY", "").strip()
#         if not api_key:
#             raise ValueError(
#                 "GROQ_API_KEY not set.\n"
#                 "1. Get a free key at https://console.groq.com\n"
#                 "2. Open your .env file and set: GROQ_API_KEY=your_key_here\n"
#                 "3. Restart Streamlit"
#             )
#         _client = Groq(api_key=api_key)
#     return _client


# def call_llm(
#     system_prompt: str,
#     user_prompt: str,
#     temperature: float = 0.5,
#     max_tokens: int = 1024,
#     model: str = "llama-3.3-70b-versatile",
# ) -> str:
#     client = get_client()
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt},
#         ],
#         temperature=temperature,
#         max_tokens=max_tokens,
#     )
#     return response.choices[0].message.content.strip()


# def call_llm_large(
#     system_prompt: str,
#     user_prompt: str,
#     temperature: float = 0.6,
#     max_tokens: int = 4096,
# ) -> str:
#     """Uses llama-3.3-70b-versatile for high quality synthesis. Falls back to 8b."""
#     for model in ["llama-3.3-70b-versatile", "llama-3.3-70b-versatile"]:
#         try:
#             return call_llm(
#                 system_prompt,
#                 user_prompt,
#                 temperature=temperature,
#                 max_tokens=max_tokens,
#                 model=model,
#             )
#         except Exception as e:
#             last_error = e
#             continue
#     raise last_error

import os
from groq import Groq

_client = None


def _load_env():
    """Load .env file manually — robust version."""
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".env"
    )

    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                if "=" in line:
                    key, _, value = line.partition("=")

                    key = key.strip()
                    value = value.split("#")[0].strip()  # remove inline comments
                    value = value.strip('"').strip("'")

                    if key and value:
                        os.environ[key] = value  # ✅ always override


def get_client() -> Groq:
    global _client
    if _client is None:
        _load_env()
        api_key = os.environ.get("GROQ_API_KEY", "").strip()

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not set.\n"
                "1. Get a free key at https://console.groq.com\n"
                "2. Open your .env file and set: GROQ_API_KEY=your_key_here\n"
                "3. Restart your app"
            )

        _client = Groq(api_key=api_key)

    return _client


def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.5,
    max_tokens: int = 1024,
    model: str = "llama-3.1-8b-instant",  # ✅ stable default
) -> str:
    client = get_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()


def call_llm_large(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.6,
    max_tokens: int = 4096,
) -> str:
    """Uses best available model with fallback."""

    models = [
        "llama-3.1-70b-versatile",   # high quality
        "llama-3.1-8b-instant",      # fast fallback
    ]

    last_error = None

    for model in models:
        try:
            return call_llm(
                system_prompt,
                user_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                model=model,
            )
        except Exception as e:
            last_error = e
            continue

    raise last_error