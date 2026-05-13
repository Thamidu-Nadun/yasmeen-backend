import unittest

EMAIL_CONTENT_EN = """
Subject: Tour Details Submission

Mr. Minagawa,
Thank you very much for your help. I sent you the following email yesterday.
It appears that the email has not arrived, so I will resend. (In the past, there have been rare cases where mail sent to Outlook has not been delivered.)
I would appreciate it if you could confirm this. Thank you very much.
Okabe

Mr. Masayo Minagawa,
Sorry to keep you waiting.
Currently, we will proceed with the tour as outlined below.
We would appreciate it if you could refer to this.
If you would like to make any changes, please let us know.

━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Booking Information]

Customer    Name: Mr. Minagawa

Start Date: 2026-05-19

End Date: 2026-05-23

Number of Pax: 02

Booking Staff: Mayumi Okabe

[Staff Assignment]

- JP Guide: Mr. Nakamoto
- EN Guide: Mr. Kasun Kottawa

Vehicle Type: Van

━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Route Plan / Itinerary]
The time schedule is only an estimate. This may change depending on road conditions and weather.

---        
19-Sep, 11:30am バンダラナイケ国際空港よりご送迎開始→
14:00pm ピンナワラ象の孤児院観光（象の川の水浴びイベントなど）→
15:30pm 同上出発→
18:30pm Heritance Kandalama 泊。
---
20-Sep, 9:00am ホテルチェックアウト→
9:50am ご主人様をロック周辺のカフェなどにご案内後、1名様がシーギリヤロック観光
（所要約2時間前後）→
12:00pm頃、 ご観光後、皆様で合流。シーギリヤロックビューポイントから撮影→
15:00pm キャンディ市内観光（例：仏歯寺、Sri Dalada museum、
キャンディビューポイントで撮影など）→
夕方、キャンディ市内 The Radh Hotel泊。
---
21-Sep, 9:00am ホテルチェックアウト→
11:30am ルート上のラブーケリーティーセンター＆紅茶工場見学（茶園鑑賞、お
茶摘み体験、カフェ、工場見学など）→
1400pm ヌワラエリヤタウンドライブ（郵便局外観、グレゴリー湖など）→
15:00pm ヌワラエリヤタウン出発→
16:50pm頃、バンダーラウェラ泊。（Manor House Bandarawela By Seven Angels）
---
22-Sep, 9:00am ホテル出発→
10:40am Lipton’s Seatに到着。車寄せの可能なポイントまでは移動可能。
（Lipton’s Seat の頂上のビューポイントへは未舗装で車いすでのご移動は
困難かもしれませんがLipton’s Seat自体に行くことは可能です。）
11:30am頃、同上出発→途中から高速道路使用→
15:30-16:00pm Weligama Bay Marriott Resort & Spa泊。
※コッガラのウミガメ保護センターに子ガメの放流スケジュールを確認。
当日夕方もしくは翌朝に観察可能ならご案内。
---
23-Sep, 11:00am頃、ホテルチェックアウト→
高速道路使用→
12:00pm ゴール市内にてランチ休憩とタウンドライブ→
14:00pm頃 ゴール市内出発。高速道路使用（途中サービスエリアにて小休止）→
16:30-17:00pm頃、コロンボ市内観光とご夕食*事前にご希望をお伺いいたします→
21:00pm ご夕食後、コロンボ市内出発。高速道路使用→
22:00pm バンダーラナーヤカ国際空港にてご送迎終了。

━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Requests]

- Supermarket
- Tea shops (including factory outlet stores)
- Local markets / fruit shops
- Ceramics outlet stores (such as Noritake, etc.)

━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Pricing / Costs]

Taxi Charter Fee (rental of one vehicle): Japanese-speaking guide and driver / AC Sedan 
Total Fee = 125,130 JPY (tax included)

Included in the quotation: Fuel costs, driver's food and drink/accommodation, toll road fees, parking fees at various locations, all guided admission fees

Not included in the quotation: Customers' food and drink, accommodation expenses, tourist attraction admission fees, tips for drivers, Ayurveda experience fee, activity fee

For the latest info on tourist attraction fees: https://tours.yasmeen.jp/s-projects-side-by-side

Tips for long-distance drivers: https://tours.yasmeen.jp/services-7

Cancellation policy: https://www.secure-cloud.jp/sf/business/1474718264jIakYEFk

━━━━━━━━━━━━━━━━━━━━━━━━━━━
Payment Method: Credit Card

━━━━━━━━━━━━━━━━━━━━━━━━━━━
If you have any other questions, please feel free to contact us.
We would appreciate your kind consideration.

Operator: Mayumi Okabe
YASMEEN TRAVELS / Yasmin Travels [E-TOURS]
20, Jayapura, Kottawa, Pannipitiya, Colombo 10230, SRI LANKA
TEL: +94-719-781781 (Japanese support)
"""

class TestEmailParser(unittest.TestCase):
    def test_parse_email_content_en(self):
        from app.utils.email_parser import extract_email_data
        data = extract_email_data(EMAIL_CONTENT_EN)
        
        self.assertIsNotNone(data)
        
        self.assertEqual(data.customer_name, "Mr. Minagawa")
        self.assertEqual(data.start_date, "2026-05-19")
        self.assertEqual(data.end_date, "2026-05-23")
        self.assertEqual(data.total_pax, 2)
        self.assertEqual(data.vehicle_type, "Van")
        self.assertEqual(data.operator_name, "Mayumi Okabe")
        self.assertEqual(data.total_fee, 125130)
        self.assertIn("Supermarket", data.requests)
        
    @unittest.skip("Japanese email parsing test not implemented yet")    
    def test_parse_email_content_jp(self):
        pass

if __name__ == '__main__':
    unittest.main()

