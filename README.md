# How to migrate to AWS Serverless application
<img src="lab-guide/images/TechSummitMacau_white_Logo.png" width=420>

## WELCOME! ##
This workshop content will handle the server based Python Flask web application and show how to migrate to Serverless architecture application using AWS Chalice micro-framework. It deals with how to migrate from a server-based application into a serverless environment by practical application level. This workshop cover Cloud9, S3, API Gateway, Lambda, Cognito, DynamoDB, X-Ray, Parameter Store with AWS Chalice micro-framework. This workshop contains two short presentations and three hands-on labs. Application source code and hands-on lab guides are providing via Github repository.

### Presenters
 * Sungshik Jou (Technical Trainer)
 * JinUk Lee (Technical Trainer)

### Lab Instructors
Thanks to the following people for their assistance with this lab:
 * KyoungSu Lee (ProServ)
 * Sungmin Hong (Technical Trainer)
 * ChungHo Min (Technical Trainer)
 * Dayoungle Jun (Technical Trainer)

## LAB GUIDE
* [LAB 01 - Take a look around](lab-guide/LAB01.md)
	* [TASK 1. Create AWS Cloud9 environment and explore the environment.](lab-guide/LAB01.md#task-1-create-aws-cloud9-environment-and-explore-the-environment)
	* [TASK 2. Look around legacy application and try run it.](lab-guide/LAB01.md#task-2-look-around-legacy-application-and-try-run-it)
	* [TASK 3. Connect to your application (Cloud9)](lab-guide/LAB01.md#task-3-optional-task-connect-to-your-application-ssh-tunneling)
	* [TASK 3 [OPTIONAL-TASK]: Connect to your application (SSH Tunneling)](lab-guide/LAB01.md#task-3-optional-task-connect-to-your-application-ssh-tunneling)
	* [TASK 4. Take a look around](lab-guide/LAB01.md#task-4-take-a-look-around)
	* [TASK 5. Challenges (Optional)](lab-guide/LAB01.md#task-5-challenges-optional)
	* [TASK 6. Stop your application](lab-guide/LAB01.md#task-6-stop-your-application)

* [LAB 02 - Move to serverless](lab-guide/LAB02.md)
	* [TASK 0. Permission grant for Cloud9](lab-guide/LAB02.md#task-0-permission-grant-for-cloud9)
	* [TASK 1. Go to DynamoDB](lab-guide/LAB02.md#task-1-go-to-dynamodb)
	* [TASK 2. Go to S3](lab-guide/LAB02.md#task-2-go-to-s3)
	* [TASK 3. Go to Cognito](lab-guide/LAB02.md#task-2-go-to-s3)
	* [TASK 4. Go to X-ray](lab-guide/LAB02.md#task-2-go-to-s3)

* [LAB 03 - Serverless with AWS Chalice](lab-guide/LAB03.md)
	* [TASK 1 : Setup virtualenv.](lab-guide/LAB03.md#task-1--seyup-virtualenv)
	* [TASK 2 : Build a simple AWS Chalice serverless app.](lab-guide/LAB03.md#task-2--build-a-simple-aws-chalice-serverless-app)
	* [TASK 3 : CloudAlbum with AWS Chalice](lab-guide/LAB03.md#task-3--cloudalbum-with-aws-chalice)