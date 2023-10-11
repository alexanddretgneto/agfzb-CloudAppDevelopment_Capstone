const fs = require('fs').promises;
const path = require('path');

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

// Função principal para obter a lista de bancos de dados
async function main(params) {
    try {
        const { COUCH_URL, IAM_API_KEY } = await readCredentials();

        const cloudant = initializeCloudant(COUCH_URL, IAM_API_KEY);
        const dbs = await getDatabases(cloudant);
        return { dbs };
    } catch (error) {
        console.error('Erro:', error);
        return { error: 'Erro ao buscar a lista de bancos de dados.' };
    }
}

// Função para inicializar o cliente Cloudant
function initializeCloudant(url, apiKey) {
    const authenticator = new IamAuthenticator({ apikey: apiKey });
    const cloudant = CloudantV1.newInstance({
        authenticator,
        serviceUrl: url,
    });
    return cloudant;
}

// Função para obter a lista de bancos de dados
async function getDatabases(cloudant) {
    try {
        const response = await cloudant.getAllDbs();
        return response.result;
    } catch (error) {
        console.error('Erro ao obter a lista de bancos de dados:', error);
        throw error;
    }
}

// Função para ler as credenciais do arquivo .creds-sample.json no diretório pai
async function readCredentials() {
    try {
        const credentialsPath = path.join(__dirname, '..', '..', '.creds-sample.json');
        const fileData = await fs.readFile(credentialsPath, 'utf-8');
        const credentials = JSON.parse(fileData);
        return credentials;
    } catch (error) {
        console.error('Erro ao ler as credenciais do arquivo:', error);
        throw error;
    }
}

main().then(console.log).catch(console.error); // Para executar a função principal
