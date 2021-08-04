import boto3
from botocore.exceptions import ClientError
import concurrent.futures
import threading 
import sys

AMAZON = "https:://s3.us-west-2.amazonaws.com"

# Running this script may result in charges for AWS Transcription. 
#
# This script goes through the whole bucket looking for audio files 
#  that do not have coreesponding files named with a .json extension.

# Searches AWS bucket for audio files without corresponding transcription
# files, then submits all, in parallel, to AWS transcription. 
# The resultng json files are put with the source. 

# Install the AWS cli tools and boto3 



# Amazon AWS call for bucket files list
#
def list_files(bucket):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(
        Bucket=bucket
    )
    print(response)
    return response


# Get list of files that have been completed for exclusion
#
def get_completed_list(response):
    done_list = []
    for i in response['Contents']:
        if i['Key'].endswith('json'):
            done_list.append(i['Key'])
    return done_list


# Test candidates for exclusion from processing
#
def clean_file(item, done_list): 
    for i in done_list:
        if i.startswith(item): # completed result file name has '.json' appended
            return(False)
    return(True)


# Create metadata for processing
# Amazon may be able to detect media format
def collect_for_processing(bucket):
    response = list_files(bucket)
    done_list = get_completed_list(response)
    todo_list = []
    for i in response['Contents']:
        if i['Key'].lower().endswith('m4a'): # for me m4a container holds mp4 TODO
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'mp4',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('mp4'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'mp4',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('mp3'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'mp3',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('wav'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'wav',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('flac'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'flac',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('ogg'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'ogg',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('amr'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'amr',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
        elif  i['Key'].lower().endswith('webm'):
            if clean_file(i['Key'], done_list):
                todo_list.append({'Key': i['Key'], 'MediaFormat':'webm',
                    'OutputBucketName':bucket,'OutputKey':i['Key']+'.json'})
    return todo_list


# submit one job to AWStranscription
#
def submit_transcription(args):
    ts = boto3.client("transcribe") # for thread safe, one call per client
    #job_uri = 's3://' + args['OutputBucketName'] + '/' + args['Key']
    job_uri = AMAZON + args['OutputBucketName'] + '/' + args['Key']
    job_name = args['Key'].split('/')

    try:
        result = ts.start_transcription_job(
                TranscriptionJobName=job_name[-1],
                Media={'MediaFileUri': job_uri},
                MediaFormat=args['MediaFormat'],
                LanguageCode='en-US',
                OutputBucketName=args['OutputBucketName'],
                OutputKey=args['OutputKey']
        )
        #print(result)
    except ClientError as e:
        print(e)
        raise e


# submit transcriptions in parallel
# On Windows, max_workers must be 61 or less
def process_list(args): 
    i = 0
    while i < len(args):
            submit_transcription(args[i])
            i += 1



    #with  concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #    executor.map(submit_transcription,args)


# Arguments bucket
# skips completed jobs, does whole direcotry. 
# Parallel dispache to Amazon.

if __name__ == "__main__":
    todo_list = collect_for_processing(sys.argv[1])
    process_list(todo_list)

