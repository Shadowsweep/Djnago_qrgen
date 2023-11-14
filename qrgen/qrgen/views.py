from django.http import HttpResponse
from django.shortcuts import render
from qrcode import *
# data = None
import os
import cv2
import numpy as np
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# def home(request):
#     global data
#     if request.method == 'POST':
#         data = request.POST['data']
        
#         img = make(data)
#         img.save('static/image/test.png')
#     else:
#         pass
#     return render(request,'home.html',{'data':data})
    
# def home(request):
#     if request.method == 'POST':
#         data = request.POST['data']
#         if not os.path.exists('static/image'):
#             os.makedirs('static/image')
#         img = make(data)
#         img.save('static/image/qr_code.png')
#         return render(request, 'home.html', {'data': data},{"message":"Record Submitted Successfully  now click on List icon at top right "})
#     else:
#         return render(request, 'home.html', {})


def home(request):
    if request.method == 'POST':
        data = request.POST['data']
        if not os.path.exists('static/image'):
            os.makedirs('static/image')
        img = make(data)
        img.save('static/image/qr_code.png')
        message = "Qr Created successfully"
        return render(request, 'home.html', {'data': data, 'message': message})
    else:
        return render(request, 'home.html', {})
    
def scan(request):
    return render(request, 'qrreader.html')
 
    
def qr_scanner(request):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    while True:
        _, img = cap.read()
        data, _, _ = detector.detectAndDecode(img)

        if data:
            a = data
            break

        cv2.imshow('QR Code Scanner', img)

        if cv2.waitKey(1) == ord('q'):
            break

    b = webbrowser.open(str(a))
    cap.release()
    cv2.destroyAllWindows()

    return render(request, 'qrreader.html', {'qr_content': a})



@csrf_exempt
def process_webcam_stream(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        webcam_image = data['image']

        # Decode QR code from the webcam image
        qr_code_data = decode_qr_code(webcam_image)

        # Return the QR code data or an error message
        if qr_code_data:
            return JsonResponse({'qr_code_data': qr_code_data})
        else:
            return JsonResponse({'error': 'QR code not found'})

    return JsonResponse({'error': 'Invalid request'})

def decode_qr_code(webcam_image):
    # Convert webcam image data to OpenCV format
    image_bytes = base64.b64decode(webcam_image)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Detect and decode QR code from the image
    detector = cv2.QRCodeDetector()
    _, _, decoded_data = detector.detectAndDecode(image)

    return decoded_data



   