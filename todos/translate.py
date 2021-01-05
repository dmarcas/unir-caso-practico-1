import os
import json
import boto3
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translation = boto3.client('translate') 
#boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
comprehend = boto3.client('comprehend') 

def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    #Recover text from table
    textToTranslate = result['Item']['text']

    #Recover text from path
    targetLanguage = event['pathParameters']['language']

    #detect main language stored
    #comprehendResponse = comprehend.detect_dominant_language(Text=textToTranslate) 
    #language = comprehendResponse['Languages'][0]['LanguageCode']

    #text translation
    #textTranslated = translation.translate_text(Text = textToTranslate, SourceLanguageCode=language, TargetLanguageCode = targetLanguage)

    #add translated text into item to be returned
    result['Item']['text'] = translateText(textToTranslate, targetLanguage) #textTranslated.get('TranslatedText')

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
    
    def translateText(textToTranslate, targetLanguage) :
        textTranslated = textToTranslate
        comprehendResponse = comprehend.detect_dominant_language(Text=textToTranslate) 
        
        if not textToTranslate
            print("Error, the text to be translated is empty")
        else if not comprehendResponse
            print("Error recovering original language ")
        else
            language = comprehendResponse['Languages'][0]['LanguageCode']
            textTranslated = translation.translate_text(Text = textToTranslate, SourceLanguageCode=language, TargetLanguageCode = targetLanguage)
            textTranslated.get('TranslatedText')
        return textTranslated
