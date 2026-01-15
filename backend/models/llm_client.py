import openai
import anthropic
import json
import os
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    """Handle OpenAI and Claude API calls for categorization"""

    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

        # Load prompt template
        with open('config/llm_prompt.txt', 'r') as f:
            self.prompt_template = f.read()

        # Load taxonomies
        with open('config/taxonomies.json', 'r') as f:
            self.taxonomies = json.load(f)

    def categorize_with_openai(self, item):
        """Use OpenAI to categorize an item"""
        prompt = self._build_prompt(item)

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a product analyst. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2500
            )

            result = json.loads(response.choices[0].message.content)
            result['model'] = 'gpt-4o'
            result['success'] = True
            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': 'gpt-4o'
            }

    def categorize_with_claude(self, item):
        """Use Claude to categorize an item"""
        prompt = self._build_prompt(item)

        try:
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=4096,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            result = json.loads(response.content[0].text)
            result['model'] = 'claude-sonnet-4-5'
            result['success'] = True
            return result

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'model': 'claude-sonnet-4-5'
            }

    def _build_prompt(self, item):
        """Build prompt from template with item data"""
        return self.prompt_template.format(
            request=item.get('Product/feature request', item.get('Customer need', '')),
            need=item.get('Customer need', ''),
            description=item.get('Need description', ''),
            source_file=item.get('source_type', ''),
            source_category=item.get('llm_context', {}).get('pmm_product_area', ''),
            other_fields=json.dumps(item.get('llm_context', {}), indent=2)
        )
