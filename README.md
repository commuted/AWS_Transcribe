## Use to submit voice recordings to Amazon AWS Transcribe.

*Source files from Amazon bucket.

*Files have extensions of [m4a, mp4, mp3, wav, flac, ogg, amr, webm]

*Results are put with source, '.json' extension is added.

*The bucket is checked for completed transcriptions which are excluded from the submission

*Audio files are submitted concurrently

*The whole bucket is searched


Command:

python transcribe.py mybucket



#         Charges apply

Setup AWS cli tools
  https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-cli.html

Setup BOTO3
  https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html


Create bucket:

aws s3api create-bucket --bucket "my-bucket" --region us-west-1 --create-bucket-configuration LocationConstraint=us-west-1

Copy voice recording:

aws s3 cp audio-file.mp4 s3://my-bucket





