# LAB 01 - Hands-on lab (30min) : Take a look around

## Configure your AWS Cloud9
In this hands-on lab, you'll configure the AWS [Cloud9](https://aws.amazon.com/cloud9/) service to look around legacy application. You can run application 'CloudAlbum' in the AWS Cloud9 EC2 instance.

## TASK 1. Create AWS Cloud9 environment and explore the environment.

In this section, you will create an AWS Cloud9 environment and explore the environment.

[1] In the AWS Console, click **Services**, then click **Cloud9** to open the Cloud9 dashboard.

[2] You can choice **Singapore** region.

[3] Click **Create environment** at the top-right corner.

[4] For **Name**, type **TechSummit-workshop**

[5] Click Next step.

[6] On the **Configure settings** page, leave the default selection in the Environment settings section.

* Click Next step.
* Review the details and click **Create environment**. This should launch your AWS Cloud9 environment in a few minutes.
* Upon environment creation, notice the terminal window on the bottom pane. The terminal provides a remote login to the instance on which the AWS Cloud9 environment is hosted, just as you used SSH for remote login in the third exercise. A pre-authenticated AWS CLI is installed in your terminal.
* Explore the terminal by typing this command: 

```
aws ec2 describe-instances
```



