from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SnippetSerializer

snippets = [
    {
      "id": 1,
      "language": "Python",
      "code": "print('Hello, World!')"
    },
    {
      "id": 2,
      "language": "Python",
      "code": "def add(a, b):\n    return a + b"
    },
    {
      "id": 3,
      "language": "Python",
      "code": "class Circle:\n    def __init__(self, radius):\n        self.radius = radius\n\n    def area(self):\n        return 3.14 * self.radius ** 2"
    },
    {
      "id": 4,
      "language": "JavaScript",
      "code": "console.log('Hello, World!');"
    },
    {
      "id": 5,
      "language": "JavaScript",
      "code": "function multiply(a, b) {\n    return a * b;\n}"
    },
    {
      "id": 6,
      "language": "JavaScript",
      "code": "const square = num => num * num;"
    },
    {
      "id": 7,
      "language": "Java",
      "code": "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}"
    },
    {
      "id": 8,
      "language": "Java",
      "code": "public class Rectangle {\n    private int width;\n    private int height;\n\n    public Rectangle(int width, int height) {\n        this.width = width;\n        this.height = height;\n    }\n\n    public int getArea() {\n        return width * height;\n    }\n}"
    }
]

@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        lang = request.query_params.get('lang')
        if lang:
            lang = lang.lower()
            filtered_snippets = []
            for snippet in snippets:
                if snippet['language'].lower() == lang:
                    filtered_snippets.append(snippet)
        else:
            filtered_snippets = snippets
        return Response(filtered_snippets)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            snippet = {
            'id': len(snippets) + 1,
            'language': serializer.validated_data['language'],
            'code': serializer.validated_data['code']
        }
        snippets.append(snippet)
        return Response(snippet, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def snippet_detail(request, pk):
    snippet = next((snippet for snippet in snippets if snippet['id'] == pk), None)
    if snippet is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(snippet)