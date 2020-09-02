# Clean Lambda Old Versions

AWS limits the total code storage for Lambda functions to 75GB.

The main reason of reaching such size is because for every deployment of existing function, AWS stores the previous version ("qualifier").

Usually, when you reach that point, you want to remove old version. This tool will help you to!

