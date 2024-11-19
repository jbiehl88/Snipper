from rest_framework import serializers

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField()
    language = serializers.CharField(max_length=50)

class UserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()