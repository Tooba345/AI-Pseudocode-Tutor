import subprocess


class ClaudeClient:

    def __init__(self):
        self.conversation = []

    def ask(self, prompt, image_path=None):

        try:
            # Add the new user message to conversation history
            self.conversation.append(
                f"USER:\n{prompt}"
            )

            # Build conversation context
            conversation_text = "\n\n".join(
                self.conversation
            )

            if image_path:
                full_prompt = (
                    "You are continuing a tutoring conversation.\n\n"
                    f"{conversation_text}\n\n"
                    f"IMPORTANT: Also analyze the image located at:\n"
                    f"{image_path}\n\n"
                    "Use the image together with the conversation "
                    "to answer the student's latest question."
                )
            else:
                full_prompt = (
                    "You are continuing a tutoring conversation.\n\n"
                    f"{conversation_text}\n\n"
                    "Answer the student's latest question while "
                    "using the previous conversation for context."
                )

            result = subprocess.run(
                ["claude", "-p", full_prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120
            )

            if result.returncode != 0:

                error = result.stderr.strip()

                if not error:
                    error = "Claude returned an unknown error."

                return f"❌ Claude error:\n{error}"

            if result.stdout is None:
                return "❌ Claude returned no response."

            response = result.stdout.strip()

            # Save Claude's response to the conversation
            self.conversation.append(
                f"ASSISTANT:\n{response}"
            )

            return response

        except subprocess.TimeoutExpired:

            return "⏳ Claude took too long to respond."

        except FileNotFoundError:

            return (
                "❌ Claude command was not found. "
                "Make sure `claude --version` works."
            )

        except Exception as e:

            return f"❌ Could not connect to Claude:\n{e}"