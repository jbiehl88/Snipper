from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SnippetSerializer, UserSerializer
from .utils import encrypt_content, decrypt_content
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

snippets = [
    {
      "id": 1,
      "language": "Python",
      "code": "gAAAAABnPPLDxGaUCMDrU6V4m2-XynskQbaCGm211426r5Ux_OyoRClMMZbYyPBZG3_BtYCPli_Uy0iT1rarX9ig-ZSdxN2TYZ08PCcK4KzsBHHBTv52X0c="
    },
    {
      "id": 2,
      "language": "Python",
      "code": "gAAAAABnPPML60NhI9HQzcwaGfwAvT3osM8r1cKSzHvMiIFqtnasmX1Z5cBdS7bSkYbjnI207D2cDGRkfiJu6Obx5hOIiG-84GpxN3puiub7syLeN7By-gc="
    },
    {
      "id": 3,
      "language": "Python",
      "code": "gAAAAABnPPO8KjEvWRfbzHtASiDJyZOJ-Q2TPB6T1zB7GsKo6M68CT00AaoaDnTnbO21ggdzTWrsJv3WRpvwisCjh-L8ruYmPv38e9An-7YcASt9jg0oKJlFZtfu1laHHxaWWD1szdeEf4gD40cTMdpQrXv7Zgsm8MjGgUOmO5zOhjgPJ4V18Xg19PN7mmF0SpfihgZREfAOoj2t1AjCj2D2jMlDKdVMcu-t7lGvHap_McV8hCAMQbTndXTJTo0SQKIkgi2gGAnk"
    },
    {
      "id": 4,
      "language": "JavaScript",
      "code": "gAAAAABnPPO83UdQXe87T7ua81PyQk6t2w8O2B487AIVaDi3SAA5zgyvmRvo52vf6_1LAoKsJTjIoUAwoFN_zIO63yf1S2aPaDXKvZm6wAPk5L0JmnRT37g="
    },
    {
      "id": 5,
      "language": "JavaScript",
      "code": "gAAAAABnPPO881EGNVYUmi7yWHDy611QI4nO-gkv8oip02NM9qv07MjLaJetk7aiEs0Qx3bCY37zsJeveh91ydoUh7sFbfXBcTcA1aTzMEqCuRaBG9MQjyGThEpGX9GCyQF6sEf0Xcxg"
    },
    {
      "id": 6,
      "language": "JavaScript",
      "code": "gAAAAABnPPO87KEpKLLyDE_ArSNNfb1YPCCaIC38hcWZ_d76G1TXxeZSGO0Rcadu5TGW9MjOQkdSwpauBW-2nYVx4DWqasecBl--i01OykMs1MC6mgYH7r0-uxTDtbc3wC8GL6ftvo37"
    },
    {
      "id": 7,
      "language": "Java",
      "code": "gAAAAABnPPO8Lix3PueV1k5IUNVAK2SN329t5ot1A1nNiNtO2mpJDAeG2sRw8t4JMBvX4rQ-CrTbktm8zI9n4OsvH78OGycMe9wFFk8X5yoAVQIZpe0NNjWv4s8jMegwVHHKCBDocFwugchATOPNvXeBZ1AYAma66syt_aWoxtiM5Pf58dP4W8NX5qgnr98_ZXwmE5bcKtGLoJxevGaaZoH750RTZ-Y_H-pvJhh0N-FfiYDfPZegW8Q="
    },
    {
      "id": 8,
      "language": "Java",
      "code": "gAAAAABnPPO8bUJJkf2FHQxqbe7XHlH0jfmJFOYqSwmxLstOaJuMt78xwCaXpXuq0hfwVRlx25MeWhssOTX-Zr6N3jApyEKMuSUePcJndBKi4Cq3GHuBh77bhWCx1AVpK590MewOuvgMvcmVs3P8qFcTrdwZ6DseTlLplIGp57R_KGqt2eBKEFg4Gz-pDsKzaY8DIg1qFKq60_4NEHfs6K70pVTNY5hXhs0ARENc9X2ybsTILNtBb1P2yyoqXvipRvjbqqQPIz5SuA1vDiQFoK5-yR6HjUuvqFHYNmPa3sD00e_QZvRNLKA7Sb0cbyacf5iaNuISLwdEa8A2CkdYzsXuIGqMUPPuydvtnXxFWhPfYc_76QdHOT-y_W_2Lj6tBv3IXvu4UTd9KiElFUfWznNe45KAB-iCuQ=="
    }
]

users = []

@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        lang = request.query_params.get('lang')
        if lang:
            lang = lang.lower()
            filtered_snippets = []
            for snippet in snippets:
                if snippet['language'].lower() == lang:
                    snippet['code'] = decrypt_content(snippet['code'])
                    filtered_snippets.append(snippet)
        else:
            filtered_snippets = [
                {**snippet, 'code': decrypt_content(snippet['code'])}
                for snippet in snippets
            ]
        return Response(filtered_snippets)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            encrypted_code = encrypt_content(serializer.validated_data['code'])
            snippet = {
            'id': len(snippets) + 1,
            'language': serializer.validated_data['language'],
            'code': encrypted_code
        }
        snippets.append(snippet)
        return Response(snippet, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def snippet_detail(request, pk):
    snippet = next((snippet for snippet in snippets if snippet['id'] == pk), None)
    if snippet is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    decrypted_snippet = {**snippet, 'code': decrypt_content(snippet['code'])}
    return Response(decrypted_snippet)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password before saving
        hashed_password = make_password(serializer.validated_data['password'])

        # Create the user object with the hashed password
        user = {
            'id': len(users) + 1,
            'email': serializer.validated_data['email'],
            'password': hashed_password
        }
        users.append(user)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user_in_db = next((u for u in users if u['email'] == email), None)

        if user_in_db and check_password(password, user_in_db['password']):
            payload = {
                'id': user_in_db['id'],
                'email': user_in_db['email'],
                'exp': datetime.now(timezone.utc) + timedelta(hours=24),
                'iat': datetime.now(timezone.utc)
            }

            secret_key = os.getenv("SECRET_KEY")
            # Encode the payload using the secret key to create the token
            token = jwt.encode(payload, secret_key, algorithm='HS256')

            print(f"Generated Token: {token}")

            return Response({
                "message": f"Account for {email} was successfully created!",
                "token": token
            }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET method for retrieving user info (requires JWT authentication)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    print("*******HELLO******")
    auth = request.headers.get('Authorization')
    if not auth:
        return Response({"error": "Authorization header missing"}, status=status.HTTP_400_BAD_REQUEST)

    token = auth.split(' ')[1]  # Extract token from Authorization header
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

    # Find the user based on the email in the payload
    user_email = payload.get('email')
    user = next((u for u in users if u['email'] == user_email), None)
    
    if user:
        return Response({"email": user['email'], "id": user['id']})
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)