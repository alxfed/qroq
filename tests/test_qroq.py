# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import unittest
import os
import sys

# Add src to sys.path to easily import qroq without installing it
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from qroq.main import respond


class TestQroqMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Read the .env file from the root directory
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

    def test_respond_basic(self):
        """Test a basic request to the API."""
        api_key = os.environ.get('GROQ_API_KEY')
        self.assertIsNotNone(api_key, "GROQ_API_KEY is not set in the environment or .env file.")

        messages = [{"role": "user", "content": "Just say the exact phrase 'Hello user' and nothing else."}]
        instruction = "You are a helpful test assistant."

        thoughts, text = respond(messages, instruction)

        # Determine if the API returned an error (which the library handles by returning empty strings)
        self.assertNotEqual(text, '', "The response text was empty, which indicates an HTTP or network error.")

        # Verify the structure/types
        self.assertIsInstance(thoughts, str)
        self.assertIsInstance(text, str)

        # Expecting at least 'hello' in the output
        self.assertIn("hello user", text.lower())


if __name__ == '__main__':
    unittest.main()
