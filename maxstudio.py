import requests
import time

API_KEY = '' # maxstudio.ai API key

def generate_baby(father_image, mother_image, gender):
    payload = {
        'fatherImage': father_image,
        'motherImage': mother_image,
        'gender': gender
    }
    try:
        response = requests.post(
            'https://api.maxstudio.ai/baby-generator',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            json=payload
        )
        return response.json()
    except Exception as error:
        print('❌ Generation completed with an error:', str(error))
        raise

def get_job_status(job_id):
    """Получает статус и результат по job ID."""
    url = f"https://api.maxstudio.ai/baby-generator/{job_id}"
    try:
        response = requests.get(
            url,
            headers={'x-api-key': API_KEY}
        )
        return response.json()
    except Exception as error:
        print('❌ Error polling status:', str(error))
        raise

if __name__ == '__main__':
    father_image = '' # image link
    mother_image = '' # image link
    gender = 'babyBoy'  # 'babyBoy' or 'babyGirl'

    response = generate_baby(father_image, mother_image, gender)
    print(response)
    job_id = response.get('jobId')
    print(job_id)

    if job_id:
        print(f"🕒 Waiting for jobId generation to complete: {job_id}")
        while True:
            try:
                status = get_job_status(job_id)
                print(f"⏳ Status: {status.get('status')}")

                if status.get('status') == 'completed':
                    image_url = status.get('result', [None])[0]
                    if image_url:
                        print(f"✅ Done: {image_url}")
                    else:
                        print("⚠️ Done, but link not found")
                    break
                elif status.get('status') == 'failed':
                    print("❌ Generation completed with an error")
                    break

                time.sleep(1)
            except Exception as e:
                print("❌ Error polling status:", str(e))
                break
    else:
        print("❌ Failed to get jobId")

    if status.get('status') == 'completed' and 'result' in status:
        image_url = status['result'][0]
        print(f"✅ Image generated: {image_url}")
    else:
        print("⌛ Result not ready yet or error occurred.")
