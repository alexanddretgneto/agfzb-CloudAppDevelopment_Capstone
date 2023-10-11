const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');
const fs = require('fs'); // Importe a biblioteca fs para ler arquivos

async function main(params) {
    try {
        // Leitura do arquivo .creds-sample.json
        const credsFile = fs.readFileSync('C:\\Users\\alex_\\OneDrive\\Área de Trabalho\\codigo3\\agfzb-CloudAppDevelopment_Capstone\\functions\\.creds-sample.json', 'utf8');
        const creds = JSON.parse(credsFile);

        const authenticator = new IamAuthenticator({ apikey: creds.IAM_API_KEY });
        const cloudant = CloudantV1.newInstance({
            authenticator: authenticator,
        });
        cloudant.setServiceUrl(creds.COUCH_URL);

        let dbList = await cloudant.getAllDbs();
        return { dbs: dbList.result };
    } catch (error) {
        return { error: error.description };
    }
}

main({}).then(console.log).catch(console.error); // Chamada de exemplo
