# Django Test Project with DocuSign API

This project demonstrates how to create and sign a contract using Django and the DocuSign API. It allows a user to create a contract, sign it, and then send it via email to a recipient to sign.

## Project Workflow
The application follows this basic flow:
1. **Register**: User registers an account.
2. **Login**: User logs into the application.
3. **Home**: After login, the user is directed to the home page.
4. **Create Contract**: The user creates a contract.
5. **Success**: After contract creation, the user sees a success page.
6. **Send Email**: The contract is sent to a determined recipient to sign via email.
7. **Contract Status**: Track the contract signing status.
8. **Error**: If there is an error, it is displayed to the user.

## Contract Text
The contract text is set by default using Lorem Ipsum text, which is used throughout the app. If needed, you can find a test PDF file named `test.pdf` in the project directory.

## Configuration
All the key factors related to DocuSign configuration are in the `core/secrets.env` file.
The DocuSign username and password should be defined in the `secrets.env` file. However, due to personal privacy concerns, I have refrained from including them in the `secrets.env` file.
Due to personal privacy concerns  `core/settings.py`,  `core/secrets.env`,  `docusign_auth.py` are ignored.

In  `core/docusign_auth.py` you must have a function to send a request to API and receive an authentication code for the rest of the proccess.
There are 2 ways to get it (oauth, jwt) which for furthure information you can read the docusign Api documentation.

## DocuSign Configuration
Some key DocuSign configuration settings are placed in `core/secrets.env` and may require adjustments for your own DocuSign account.

**Important Note**: There is a minor issue in the configuration of DocuSign that I was unable to fix despite my efforts using Stack Overflow, ChatGPT, and DocuSign documentation. The issue arises when trying to create an envelope and contract, but it has not been resolved yet.

  
## Requirements
All required dependencies are listed in the `requirements.txt` file. Install them using the following command:

```bash
pip install -r requirements.txt



I would be grateful if you could identify any issues in the program and contribute your insights to help complete and enhance it.
