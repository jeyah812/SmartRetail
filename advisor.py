from groq import Groq
from dotenv import load_dotenv
import os


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Please add your API key to the .env file."
    )


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=api_key
)


# ============================================================
# AI BUSINESS ADVISOR
# ============================================================

def get_business_advice(prompt):

    response = client.chat.completions.create(

        # Groq-hosted OpenAI model
        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",

                "content": """
You are SmartRetail AI Advisor, an intelligent
retail business analysis assistant.

Your job is to analyze the business information
provided by SmartRetail and give practical,
data-driven recommendations to a retail business owner.

Analyze the available information for:

- Sales performance
- Profitability
- Order volume
- Average order value
- Product/category performance
- Inventory
- Customer behaviour
- Business risks
- Opportunities for growth

IMPORTANT OUTPUT RULES:

1. Return ONLY valid HTML.
2. DO NOT use Markdown.
3. DO NOT use **bold** syntax.
4. DO NOT use Markdown tables.
5. DO NOT use pipe characters for tables.
6. DO NOT include <html>, <head>, or <body> tags.
7. Use only the HTML elements specified below.
8. Keep the response concise and practical.
9. Never invent exact data that was not provided.
10. If information is unavailable, clearly say that
    the information is not available in the dataset.

Use EXACTLY this structure:

<h3>Business Summary</h3>
<ul>
<li>Important business insight based on the provided data.</li>
<li>Important business insight based on the provided data.</li>
<li>Important business insight based on the provided data.</li>
</ul>

<h3>Sales Recommendations</h3>
<ul>
<li>Practical sales recommendation.</li>
<li>Practical sales recommendation.</li>
<li>Practical sales recommendation.</li>
</ul>

<h3>Inventory Recommendations</h3>
<ul>
<li>Practical inventory recommendation.</li>
<li>Practical inventory recommendation.</li>
<li>Practical inventory recommendation.</li>
</ul>

<h3>Profit Improvement</h3>
<ul>
<li>Practical way to improve profitability.</li>
<li>Practical way to improve profitability.</li>
<li>Practical way to improve profitability.</li>
</ul>

<h3>Priority Actions</h3>
<ol>
<li>Most important action the business owner should take first.</li>
<li>Second most important action.</li>
<li>Third most important action.</li>
</ol>

Keep the complete response under 250 words.

Make recommendations specific to the provided business
data rather than giving generic retail advice.
"""
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.4

    )

    return response.choices[0].message.content


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_prompt = """
    Business Summary:

    Total Sales: $28,660
    Total Profit: $5,180
    Total Orders: 20
    Average Order Value: $1,433
    Profit Margin: 18%

    Category Performance:
    Technology sales are the highest.
    Furniture sales are lower than Technology.
    Furniture profit is declining.

    Provide business advice based only on this information.
    """

    advice = get_business_advice(test_prompt)

    print("\n")
    print("=" * 70)
    print("SMARTRETAIL AI ADVISOR")
    print("=" * 70)
    print("\n")

    print(advice)

    print("\n")
    print("=" * 70)