import azure.cognitiveservices.speech as speechsdk
import requests, uuid, json

def translate_text(text, target_language):
    # Azureのサブスクリプションキーとエンドポイントを設定します。
    subscription_key = ""
    endpoint = ""

    # 翻訳するテキストとターゲット言語を設定します。
    body = [{'text': text}]
    params = {
        'api-version': '3.0',
        'to': target_language
    }

    # ヘッダーを設定します。
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': 'eastus',
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # POSTリクエストを送信します。
    response = requests.post(endpoint + '/translate', params=params, headers=headers, json=body)

    # 翻訳結果を取得します。
    result = response.json()
    translated_text = result[0]['translations'][0]['text']

    return translated_text



def text_to_speech(text, output_filename):
    # Azureのサブスクリプションキーとリージョンを設定します。
    speech_key = ""
    service_region = "eastus"

    # SpeechConfigオブジェクトを作成します。
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # SpeechSynthesizerオブジェクトを作成します。
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # テキストを音声に変換します。
    result = speech_synthesizer.speak_text_async(text).get()

    # 結果をWAVファイルとして保存します。
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file(output_filename)
    else:
        print(f"Speech synthesis failed: {result.error_details}\n")

text ="""こんにちは、私はケイタです。
    趣味は、プログラミングと映画を観ること、美術館に行くことです。
    他にも色々興味あるので教えてください！
    普段は、プログラミングとセキュリティを勉強してます。それ以外の分野も色々勉強をしています。
    勉強方法はブログを書いています！どうぞよろしくお願いします。
"""

print(translate_text(text, "en"))
text_to_speech(translate_text(text,"en"), "output.wav")
