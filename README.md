# LCAbyg_WebAPI_DocumentationAndExamples
Repo for collecting the documentation and examples for the Danish software LCAbyg's WebAPI

# Quick Start guide

1. Register on https://api.lcabyg.dk/da/
2. Upon successful registration, you should use the same account username and password in the Login API (you can find it in the postman collection above) request (just replace values in the body). That access token can be then used for authentication for every other API call in the collection.
3. Example files (python & JSON) can be found in this repo and on the official website above.

4. In order to create a new Job, you should first encode a proper JSON (must be compatible with LCAbyg standard!) with base64 encoding (usind this [converter](https://codebeautify.org/json-to-base64-converter) for example) and the encoded result should be pasted as a value of "input_blob".
5. Fastest way to start a Job is to open the Job (POST) request, copy paste one of the encoded input_blobs from [this](https://github.com/3dbyggeri/LCAbyg_WebAPI_DocumentationAndExamples/tree/main/examples/input_blob_test_files) folder and Send request. (these test input_blobs are from the example JSON files provided by LCAbyg)
