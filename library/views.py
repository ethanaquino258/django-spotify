from os import error

from django.http.response import HttpResponseBadRequest
from songs.authentication import authCode
from django.shortcuts import render
from datetime import datetime, timezone
import pytz
import boto3
from botocore.exceptions import ClientError
import pandas as pd
from dynamodb_json import json_util as json


def connectToDB():
    try:
        ddb = boto3.client('dynamodb', endpoint_url='http://localhost:3000')
    except ClientError as e:
        print(e)
        exit()
    return ddb


def libraryIndex(request):
    request.session['username'] = request.POST.get('username')
    return render(request, 'library/libraryIndex.html', {'results': request.session['username']})


def libraryRead(request):
    username = request.session['username']
    dynamoClient = connectToDB()
    print('connected')
    dbCheck = dynamoClient.list_tables()

    if f'{username}_library' in dbCheck['TableNames']:
        result = dynamoClient.scan(TableName=f'{username}_library')
        genres = dynamoClient.scan(TableName=f'{username}_genres')
        if result['Count'] > 0:
            return render(request, 'library/libraryRead.html', {'results': json.loads(result['Items']), 'genres': json.loads(genres['Items'])})

    client = authCode("user-library-read", username)
    results = client.current_user_saved_tracks()
    tracks = results['items']

    while results['next']:
        results = client.next(results)
        tracks.extend(results['items'])

    trackTotal = len(tracks)

    trackCounter = 0
    # progressMarkers = multiples(trackTotal)

    utc = pytz.utc
    overallGenres = set()

    for item in tracks:
        # if trackCounter in progressMarkers:
        #     print(f'{trackCounter}/{trackTotal} analyzed...')
        artistList = []
        genreList = set()

        timeAdded = item['added_at'][:-1]
        # this outputs 2021-11-11 19:26:58.506135+00:00 format, but i want 2019-01-30T16:48:47 for uniformity. Fix later
        entryTime = str(datetime.now(timezone.utc))

        trackObj = item['track']
        trackName = trackObj['name']
        trackUri = trackObj['uri']
        for artist in trackObj['artists']:
            artistList.append(artist['name'])

            artistResult = client.artist(artist['id'])
            if artistResult['genres'] == []:
                genreResult = ['none']
            else:
                genreResult = artistResult['genres']

            for genre in genreResult:
                genreList.add(genre)

        for genresPerArtist in genreList:
            for genre in genresPerArtist:
                overallGenres.add(genre)

        print(tuple(genreList))
        try:
            response = dynamoClient.put_item(
                TableName=f'{username}_library',
                Item={
                    'id': {'N': str(trackCounter)},
                    'name': {'S': trackName},
                    'artists': {'SS': artistList},
                    'genres': {'SS': tuple(genreList)},
                    'uri': {'S': trackUri},
                    'time_addded': {'S': timeAdded},
                    'entry_time': {'S': entryTime}
                }
            )

            print(f'ITEM ADDED:\n{response}\n')
            trackCounter += 1
        except ClientError as e:
            print(e)
    result = dynamoClient.scan(TableName=f'{username}_library')
    genres = dynamoClient.scan(TableName=f'{username}_genres')
    return render(request, 'library/libraryRead.html', {'results': json.loads(result['Items']), 'genres': json.loads(genres['Items'])})

# ideally wouldn't need this second read, in prod it would just cost more capacity. Just here for testing + decoupling from the first function, although IDK if strictly necessary.
# also, prob dont need the df now that i think about it because you can just read the result directly and iterate over that...
# but hey, it works. next up is the frontend


def genreRead(request):
    username = request.session['username']
    dynamoClient = connectToDB()
    print('connected')
    result = dynamoClient.scan(TableName='aquinyo_library')
    df = pd.DataFrame(json.loads(result['Items']))
    print(df, file=open('df.txt', 'a'))

    genreDict = []
    overallGenres = set()

    for entry in df.iterrows():
        print(entry)
        print(entry[1]['genres'])
        for genre in entry[1]['genres']:
            overallGenres.add(genre)

    print(overallGenres)
    for genre in overallGenres:
        genreUris = []
        for entry in df.iterrows():
            if genre in entry[1]['genres']:
                genreUris.append(entry[1]['uri'])

        genreObj = {'genre': genre, 'occurrences': len(
            genreUris), 'uris': genreUris}
        genreDict.append(genreObj)

    idCount = 0
    for entry in genreDict:
        try:
            response = dynamoClient.put_item(
                TableName=f'{username}_genres',
                Item={
                    'id': {'N': str(idCount)},
                    'name': {'S': entry['genre']},
                    'occurrences': {'N': str(entry['occurrences'])},
                    'uris': {'SS': entry['uris']}
                }
            )
            print(f'ITEM ADDED:\n{response}\n')
            idCount += 1
        except ClientError as e:
            print(e)
