import json
import os
import re
import sys

from openai import APIError, OpenAI
from tm2p._intern import Params  # type: ignore
from tm2p.enum import ThField  # type: ignore
from tm2p.enum import ThFile  # type: ignore
from tm2p.refine._intern.data_access import load_thesaurus_as_dataframe  # type: ignore
from tm2p.refine.concept.stop import Stopword  # type: ignore

SYSTEM_PROMPT = """
You are a conservative classifier for reusable stopwords used in scientometrics, co-word analysis, and tech mining.

Your task is to determine if the current term is a domain stopword.

The curent domain is SYSTEM DYNAMICS.

Return exactly one of the following labels:

- "yes": the term is a generic or domain-specific stopword and contribute little or no give thematic information about the current domain.
- "no": keep the term.

Decision rules:

- Stopwords are terms that do not help to interpret and understand the thematic content of a document, cluster, or corpus.
- When uncertain, return "no".


OUTPUT FORMAT (STRICT — JSON ONLY):
The output MUST be a JSON object with the following structure:

{{
    "answer": "<common|scientific|no>"
}}

Any output different of this must be considered invalid. Do not include explanations, comments, 
markdown, code fences, additional keys, or any text outside the JSON object.

"""

USER_TEMPLATE = """

TERM: "{term}"


"""

CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


PREFERRED = ThField.PREFERRED.value
VARIANT = ThField.VARIANT.value


def _is_stopword(term: str) -> str:

    user_prompt = USER_TEMPLATE.format(term=term)

    try:

        response = CLIENT.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                },  # type: ignore
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )

    except APIError as e:
        raise RuntimeError(f"OpenAI API error: {e}")

    content = response.choices[0].message.content.strip()  # type: ignore
    json_text = _extract_json_text(content)

    try:
        result = json.loads(json_text)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON output from OpenAI API: {content}")

    answer = result.get("answer")
    if answer not in {"no", "yes"}:
        raise ValueError(f"Invalid answer from OpenAI API: {answer}")

    return answer


def _extract_json_text(content: str) -> str:
    """Extract JSON payload, accepting fenced markdown responses."""
    fenced_match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", content, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1).strip()
    return content


def main():

    params = Params()
    params.root_directory = "./scopus/"
    params.thesaurus_file = ThFile.CONCEPT
    df = load_thesaurus_as_dataframe(params=params)
    df = df[[PREFERRED, VARIANT]]

    df = df[~df[PREFERRED].str.startswith("#")]

    n_found = 0

    df = df[df[PREFERRED].str.len() > 3]
    df = df.reset_index(drop=True)

    for index, row in df.iterrows():

        preferred = row[PREFERRED]
        variants = row[VARIANT].split("; ")
        variants = [v.strip() for v in variants]

        sys.stderr.write(f"{index+1}/{len(df)}  Checking: {preferred}   ")
        answer = _is_stopword(preferred)
        if answer != "no":

            n_found += 1

            Stopword().having_word(preferred).where_root_directory("./scopus/").run()
            sys.stderr.write("\n")
            sys.stderr.write(f"  n = {n_found}\n")
            sys.stderr.write("\n")
        else:
            sys.stderr.write("\n")
        sys.stderr.flush()


if __name__ == "__main__":
    main()
