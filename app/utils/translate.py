from openai import OpenAI, APIStatusError
import os
from dotenv import load_dotenv
import json

load_dotenv()

AI_API_KEY = os.getenv("OPENROUTER_API_KEY") 

MODELS = [
    "openrouter/owl-alpha",
    "deepseek-v4-flash:free",
    "google/gemma-4-26b-a4b-it:free",
]


def chat_inference(system_prompt: str, user_prompt: str) -> str | None:
    if not AI_API_KEY:
        print("Error: OPENROUTER_API_KEY environment variable is not set.")
        return "Error: API key not found."
    
    for model in MODELS:
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=AI_API_KEY,
            )
            
            response = client.chat.completions.create(
                extra_headers={
                    "X-OpenRouter-Title": "Yasmeen Backend Translation Request",
                },

                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ])
            print(f"Success with model {model}")
            return response.choices[0].message.content
        
        except APIStatusError as e:
            if e.status_code == 429:
                print(f"Rate limit exceeded for model {model}. Trying next model...")
            elif e.status_code >= 500:
                print(f"Server error for model {model}. Trying next model...")
                
        except Exception as e:
            print(f"Error with model {model}")
            # print(f"Error: {e}")
        
    return "Error: All models failed to translate the text."
    

def translate_jp_to_en(text: str) -> dict | None:
    system_prompt = """
    You are a professional Japanese-to-English travel itinerary translator.

    Your task:
    1. Read the provided Japanese travel/tour text.
    2. Translate the content into natural English.
    3. Extract ONLY:
        - itinerary
        - customer requests
    4. Return ONLY raw JSON.
    5. No markdown.
    6. No explanations.
    7. No code blocks.

    JSON format:

    {
        "itinerary": [
            {
                "day": "May 10",
                "description": "10:00am Pickup from Mango House Japanese Guest House, Negombo..."
            }
        ],
        "requests": [
            "Supermarket"
        ]
    }

    Rules:
    - Keep itinerary in chronological order.
    - Preserve times, hotel names, arrows (→), and locations.
    - Translate Japanese into natural English.
    - Requests should contain shopping places and customer preferences.
    - If no requests exist, return [].
    - Return RAW JSON ONLY.

    VERY IMPORTANT:
    - Do NOT write ```json
    - Do NOT write markdown
    - Do NOT write "Translated Text:"
    - Response must be directly parseable with json.loads()
    - "iternary" MUST be an array of objects
    - Each object MUST contain EXACTLY:
        - "day" (string)
        - "description" (string)
    - Do NOT convert objects into strings
    - Do NOT flatten fields
    - Do NOT merge fields

    """
    response = chat_inference(system_prompt, text)
    return json.loads(response) if response else None


# if __name__ == "__main__":
#     data = {
#         "iternary": [
#             "スケジュール時間はあくまで目安です。道路状況や天候により変更になる場合があります。",
#             "5月10日 10:00am ネゴンボの Mango House Japanese Guest House（422/B Captain Nishendra Fernando Mawatha, Negombo）へお迎え → 2:00pm キャンディ市内到着。少し休憩後、4:45pm に仏歯寺近くの Kandy Art Association にてキャンディアンダンス鑑賞 → その後、Hanthana House（No.108, Richmond Hill Residencies, Thapodarama Road, Hanthana / TEL 077 737 4560）へ宿泊。",
#             "5月11日 午前：ホテル出発 → キャンディ市内観光（仏歯寺、Sri Dalada Museum、Giragama Tea Factory と紅茶工場・茶畑見学、キャンディビューポイントでの写真撮影など） → Hanthana House（キャンディ）宿泊。",
#             "5月12日 9:00am ホテル出発 → 12:00pm シギリヤロック近くで昼食休憩 → 1:00pm 出発 → 1:30pm ハバラナにて専用ジープへ乗り換え → 2:00pm ミンネリヤ国立公園またはシギリヤ近郊の自然公園にてジープサファリ開始（約2.5時間） → 4:30–5:00pm サファリ終了後、タクシーと合流 → Heritance Kandalama 宿泊。",
#             "5月13日 可能であれば 5:30am ホテル出発 → シギリヤロック観光（約2時間。天候によっては午後の涼しい時間帯への変更も可能） → 7:30–8:00am ホテルへ戻り、朝食と休憩 → ご希望の場合、シギリヤロックビューポイントで写真撮影 → Heritance Kandalama 宿泊。",
#             "5月14日 10:00am ホテル出発 → ※ご希望の場合、途中でダンブッラ石窟寺院へ立ち寄り可能。高速道路利用 → 2:00pm頃 コロンボ到着。アーユルヴェーダ眼科クリニック、またはご希望の場所へご案内後、ツアー終了。"
#             ],
#         "requests": [
#             "スーパーマーケット",
#             "紅茶店（ファクトリーアウトレット含む）",
#             "ローカルマーケット・フルーツショップ",
#             "陶器アウトレット店（ノリタケなど）"
#         ]
#     }
#     text = json.dumps(data, ensure_ascii=False)
#     translated_text = translate_jp_to_en(text)
#     print("Translated Text:", translated_text)
    
#     print("\n\n\nParsed JSON:")
    
#     parsed_data = json.loads(translated_text or "{}")
#     print(parsed_data)
    
