const fs = require('fs');
const path = require('path');
const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

// Determine o caminho completo para o arquivo .creds-sample.json.
const credsPath = path.join(__dirname, '..', '..', '.creds-sample.json');

// Carrega as informações do arquivo .creds-sample.json.
const creds = JSON.parse(fs.readFileSync(credsPath, 'utf8'));

async function main() {
  const authenticator = new IamAuthenticator({ apikey: creds.IAM_API_KEY });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(creds.COUCH_URL);

  try {
    const dbList = await getDbs(cloudant);
    console.log({ dbs: dbList });
  } catch (err) {
    console.error(err);
  }
}

async function getDbs(cloudant) {
  try {
    const response = await cloudant.getAllDbs();
    return response.result;
  } catch (err) {
    console.error(err);
    throw err;
  }
}

// Certifique-se de chamar a função main quando seu código for executado.
main().catch((error) => {
  console.error(error);
});
