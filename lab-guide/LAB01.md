# LAB 01 - Hands-on lab (30min) : Take a look around

## Configure your AWS Cloud9
In this hands-on lab, you'll configure the AWS [Cloud9](https://aws.amazon.com/cloud9/) service to look around legacy application. You can run application 'CloudAlbum' in the AWS Cloud9 EC2 instance.

## TASK 1. Create AWS Cloud9 environment and explore the environment.

In this section, you will create an AWS Cloud9 environment and explore the environment.

1. In the AWS Console, click **Services**, then click **Cloud9** to open the Cloud9 dashboard.

2. You can choice **Singapore** region.

3. Click **Create environment** at the top-right corner.

4. For **Name**, type **TechSummit-workshop**

5. Click Next step.

6. On the **Configure settings** page, leave the default selection in the Environment settings section.

7. Click Next step.

8. Review the details and click **Create environment**. This should launch your AWS Cloud9 environment in a few minutes.

9. Upon environment creation, notice the terminal window on the bottom pane. The terminal provides a remote login to the instance on which the AWS Cloud9 environment is hosted, just as you used SSH for remote login in the third exercise. A pre-authenticated AWS CLI is installed in your terminal.

10. Explore the terminal by typing this command: 

```
aws ec2 describe-instances
``` 
* Is it works well? Cool. Go to next stage.

```
sudo pip-3.6 install boto3
```

11. At the terminal, type **python3** and press ENTER.

12. For the confirmination, try the Python Boto 3 APIs by executing these commands:


```python
import boto3
client = boto3.client('ec2')
client.describe_instances()
```


13. Press **CTRL+D** to exit the Python interpreter.

**NOTE :** You can also use **virtualenv** for your project. Please refer following links. In this LAB doesn't user **virtualenv** for the convinience.

* https://docs.aws.amazon.com/ko_kr/cloud9/latest/user-guide/sample-python.html#sample-python-install

* https://docs.aws.amazon.com/ko_kr/cloud9/latest/user-guide/sample-python.html#sample-python-run


## TASK 2. Look around legacy application and try run it.

Check out the workshop repository from the Github.

```
cd ~/environment
git clone https://github.com/liks79/aws-chalice-migration-workshop.git
```

14. Install the requirements for the project by executing the command below in your AWS Cloud9 terminal.




