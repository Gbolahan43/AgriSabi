# Phase C: Security & Voice Edge (AWS Setup)

This guide walks you through setting up user identities securely using Amazon Cognito, and ensuring your backend IAM User has the exact permissions necessary to execute the architecture.

## 1. Amazon Cognito Setup (User & Identity Pools)
Even if the AgriSabi app is "free to all" for the MVP without a login screen, creating anonymous session identities in Cognito prevents bot abuse on your expensive Bedrock models.

### Step-by-Step Instructions:
1. Log into the AWS Console and search for **Cognito**.
2. Select **Create user pool**.
3. **Configure sign-in experience**:
   - Check **Email** and **Phone number**. 
   - Click Next.
4. **Configure security requirements**:
   - Set Password policy to **Cognito defaults**.
   - Under Multi-factor authentication (MFA), select **No MFA** (since we want frictionless access for smallholder farmers).
   - Under User account recovery, select **Email only**. Click Next.
5. **Configure sign-up experience**:
   - Keep default attribute verification. Click Next.
6. **Configure message delivery**:
   - Select **Send email with Cognito** (to save setting up Amazon SES for now). Click Next.
7. **Integrate your app**:
   - **User pool name**: Enter `agrisabi-user-pool`.
   - Under Initial app client: Check **Public client**.
   - **App client name**: Enter `agrisabi-web`.
   - **Client secret**: Select **Don't generate a client secret** (Crucial: Next.js frontend clients cannot securely store secrets).
   - Click Next, review, and click **Create user pool**.
8. **CRITICAL**: Open your new User Pool. Copy the **User pool ID** string heavily. Paste it into your `backend/.env` file as `COGNITO_USER_POOL_ID`.

*(Optional for WebRTC Audio Streaming directly from device to AWS)*:
If your frontend needs direct, temporary AWS credentials to bypass the FastAPI server for heavy audio file uploads:
1. Go to Cognito -> **Identity pools** (Federated Identities).
2. Click **Create identity pool**.
3. Choose **Guest access** to allow unauthenticated identities.
4. Let it create the default IAM Roles. Copy the **Identity pool ID** to your `.env` file as `COGNITO_IDENTITY_POOL_ID`.

---

## 2. IAM User & Execution Roles
The AWS Access Keys you placed in your `backend/.env` file belong to an IAM User. This user *must* have the correct permission boundaries to call the services we just built.

### Step-by-Step Instructions:
1. In the AWS Console search bar, type **IAM** and select it.
2. In the left menu, select **Users**.
3. Click the User you are using for AgriSabi (the one whose access keys are in your `.env`).
4. On the user's dashboard, click **Add permissions** -> **Add permissions**.
5. Select **Attach policies directly**.
6. Use the search bar to find and attach the following managed policies:
   - `AmazonBedrockFullAccess` *(Grants access to Converse, Agent, RetrieveAndGenerate)*
   - `AmazonS3FullAccess` *(Grants ability to push temporary audio files)*
   - `AmazonDynamoDBFullAccess` *(Grants ability to log sessions)*
   - `AmazonTranscribeFullAccess` *(Used for Tier-2 Native Voice routing)*
   - `AmazonPollyFullAccess` *(Used for Tier-2 Native Voice synthesis)*
7. Click **Next** and **Add permissions**.

*Security Note: For production systems, you should create an inline policy that strictly scopes these permissions down explicitly to the ARNs (Amazon Resource Names) of the exact S3 buckets and DynamoDB tables you created in Phase A, rather than `FullAccess`. For testing this locally, `FullAccess` ensures you hit no roadblocks.*

You have now fully set up your AWS Environment! Once your `.env` is loaded, AgriSabi's FastAPI orchestrator is fully weaponized.
